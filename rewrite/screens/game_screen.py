import json
import math
import random
from collections import OrderedDict
from random import randint

import pygame

from entities.planet import Planet
from screens.base_screen import Screen

# CONFIG
CHUNK_SIZE = 20000  # taille d'un chunk (px monde)
ZOOM_FACTOR = 1.1  # vitesse du zoom
SYSTEM_SPACING = 30000  # distance moyenne entre systèmes
PLANETS_PER_SYSTEM = (3, 7)  # min/max
MAX_LOADED_CHUNKS = 25  # nombre de chunks max en mémoire
SYSTEM_MIN_PLANET_DIST = (
    800  # distance minimale entre deux planètes d'un même système (optimisé)
)
GALAXY_BIOMES = ["terran", "lava", "ice", "gasgiant"]  # exemple de biomes
class GameScreen(Screen):
    def __init__(self, game, width, height, font, playerController):
        super().__init__()
        self.game = game
        self.ship = None
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.zoom_speed = 1.0  # plus grand -> zoom plus rapide
        self.playerController = playerController

        # world / procedural
        self.chunk_cache = OrderedDict()  # key (cx,cy) -> list[Planet]
        self.loaded_chunks = set()
        self.galaxy_seed = getattr(game, "galaxy_seed", None) or 123456
        self.rng = random.Random(self.galaxy_seed)

    # ===================== SHIP LOAD =====================
    def loadShip(self, ship, pos, vel, angle):
        self.ship = ship
        self.ship.pos = pygame.Vector2(pos)
        self.ship.vel = pygame.Vector2(vel)
        self.ship.angle = angle

    # ===================== CHUNK / SYSTEM GENERATION =====================
    def chunk_key_from_pos(self, pos):
        # pos: Vector2 or tuple
        x = int(pos.x if hasattr(pos, "x") else pos[0])
        y = int(pos.y if hasattr(pos, "y") else pos[1])
        return (x // CHUNK_SIZE, y // CHUNK_SIZE)

    def ensure_chunk_loaded(self, cx, cy):
        key = (cx, cy)
        if key in self.chunk_cache:
            # refresh position in OrderedDict pour LRU
            self.chunk_cache.move_to_end(key)
            return
        # génération déterministe
        seed_str = f"{self.galaxy_seed}-{cx}-{cy}"  # string concaténée
        r = random.Random(seed_str)
        systems = self.generate_systems_in_chunk(r, cx, cy)
        planets = []
        for sys in systems:
            planets.extend(sys["planets"])
        self.chunk_cache[key] = planets
        self.chunk_cache.move_to_end(key)

        # LRU eviction
        while len(self.chunk_cache) > MAX_LOADED_CHUNKS:
            evicted_key, _ = self.chunk_cache.popitem(
                last=False
            )  # supprime le plus ancien
            print(f"[Galaxy] Evicted chunk {evicted_key} from memory")

    def generate_systems_in_chunk(self, r, cx, cy):
        """Genère quelques systèmes dans le chunk; retourne liste de systèmes {center, planets, biome}"""
        systems = []
        # determine #systems via Poisson-like small random
        n_systems = r.randint(0, 2)  # 0..2 systems per chunk
        for i in range(n_systems):
            # choose system center inside chunk bounds
            base_x = cx * CHUNK_SIZE
            base_y = cy * CHUNK_SIZE
            sx = r.randint(base_x, base_x + CHUNK_SIZE - 1)
            sy = r.randint(base_y, base_y + CHUNK_SIZE - 1)
            biome = r.choice(GALAXY_BIOMES)
            planets = self.generate_planets_for_system(r, (sx, sy), biome)
            systems.append({"center": (sx, sy), "planets": planets, "biome": biome})
        return systems

    def generate_planets_for_system(self, r, center, biome):
        """Placement optimisé: on place les planètes sur orbites, spacing garanti"""
        sx, sy = center
        planets = []
        n = r.randint(PLANETS_PER_SYSTEM[0], PLANETS_PER_SYSTEM[1])
        for i in range(n):
            # orbital radius grows with index and small jitter

            
            angle = r.random() * math.tau
            px = sx + math.cos(angle)
            py = sy + math.sin(angle)
            pr = r.randint(100, 1500)
            color = (
                r.randint(60, 255),
                r.randint(60, 255),
                r.randint(60, 255),
            )
            p = Planet((px, py), pr, color)
            # small chance add suffix
            planets.append(p)
        return planets

    # ===================== UTIL to get planets around player =====================
    def get_planets_near_player(self, radius=CHUNK_SIZE * 2):
        # ensure chunks around player are loaded
        pk = self.chunk_key_from_pos(self.ship.pos)
        px, py = pk
        # load a 3x3 ring
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                self.ensure_chunk_loaded(px + dx, py + dy)
        # gather planets from those chunks
        gathered = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                key = (px + dx, py + dy)
                gathered.extend(self.chunk_cache.get(key, []))
        return gathered

    # ===================== serialization helpers for save_manager =====================
    def serialize_loaded_chunks(self):
        """Return dict: chunk_key_str -> list of planet dicts (only loaded chunks)"""
        out = {}
        for key, planets in self.chunk_cache.items():
            ck = f"{key[0]},{key[1]}"
            out[ck] = [p.to_dict() for p in planets]
        return out

    def deserialize_loaded_chunks(self, chunks_dict):
        """Load a dict produced by serialize_loaded_chunks"""
        for ck, plist in chunks_dict.items():
            cx, cy = map(int, ck.split(","))
            key = (cx, cy)
            self.chunk_cache[key] = [Planet.from_dict(d) for d in plist]

    # ===================== generatePlanets compatibility (keeps API) =====================
    def generatePlanets(self):
        """Compat: generate a few chunks around origin and return flattened planet list"""
        origin_chunk = (0, 0)
        self.ensure_chunk_loaded(*origin_chunk)
        planets = self.chunk_cache[origin_chunk]
        # store as planetList attribute for code compatibility
        self.planetList = planets
        print("[Game] Generated planets", [p.name for p in self.planetList])
        return self.planetList

    def handleEvent(self, event):
        pass

    def update(self, dt):
        # smooth zoom interpolation (exponential-like)
        # lerp target zoom with speed scaled by dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
            self.zoom = min(5.0, self.zoom + 1,2*dt)
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            self.zoom = max(0.001, self.zoom - 1,2*dt)


        # update ship physics
        controls = (
            self.playerController.getControls()
            if hasattr(self.playerController, "getControls")
            else self.playerController.getControls(self.ship)
        )
        self.ship.update(dt, controls)

        # lazy load chunks around ship
        pk = self.chunk_key_from_pos(self.ship.pos)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                self.ensure_chunk_loaded(pk[0] + dx, pk[1] + dy)

    # ===================== RENDER =====================
    def render(self, surface):
        surface.fill((10, 10, 30))
        # camera centered
        half = pygame.Vector2(surface.get_size()) / 2
        cam = self.ship.pos - half / self.zoom

        # draw planets
        planets = self.get_planets_near_player()
        for planet in planets:
            planet.render(surface, cam, self.zoom)

        # draw ship
        self.ship.render(surface, cam, self.zoom)

        # debug info
        font = self.game.fonts["default"]
        fps = font.render(f"FPS: {self.game.clock.get_fps():.1f}", True, (200, 200, 50))
        speed = font.render(f"Speed: {self.ship.vel.length():.1f}", True, (0, 255, 255))
        zoom_txt = font.render(f"Zoom: {self.zoom:.2f}×", True, (200, 200, 200))
        shipInfo = font.render(f"Ship: {self.ship.name}", True, (200, 100, 30))
        surface.blit(fps, (10, 10))
        surface.blit(speed, (10, 30))
        surface.blit(zoom_txt, (10, 50))
        surface.blit(shipInfo, (10, 70))

        # minimap (bottom-right)
        self.render_minimap(surface, cam, self.zoom)

    # ===================== MINIMAP =====================
    def render_minimap(self, surface, cam, zoom):
        # small minimap: shows planets in the local 3x3 chunk area
        w, h = surface.get_size()
        mm_w, mm_h = 200, 120
        mm_x, mm_y = w - mm_w - 10, h - mm_h - 10
        mm_rect = pygame.Rect(mm_x, mm_y, mm_w, mm_h)
        pygame.draw.rect(surface, (15, 15, 25), mm_rect)
        pygame.draw.rect(surface, (100, 100, 140), mm_rect, 2)

        # define minimap world extents: centered on ship ± VIEW (e.g., CHUNK_SIZE)
        view = CHUNK_SIZE
        left = self.ship.pos.x - view
        top = self.ship.pos.y - view
        scale_x = mm_w / (2 * view)
        scale_y = mm_h / (2 * view)

        # draw planets in the gathered area
        planets = self.get_planets_near_player()
        for p in planets:
            sx = mm_x + (p.pos.x - left) * scale_x
            sy = mm_y + (p.pos.y - top) * scale_y
            # clamp inside minimap
            if not (mm_x <= sx <= mm_x + mm_w and mm_y <= sy <= mm_y + mm_h):
                continue
            r = max(2, int(3 * (p.radius / 2000)))  # dot size by radius
            pygame.draw.circle(surface, p.color, (int(sx), int(sy)), r)

        # player dot
        px = mm_x + mm_w / 2
        py = mm_y + mm_h / 2
        pygame.draw.circle(surface, (255, 255, 255), (int(px), int(py)), 4)
