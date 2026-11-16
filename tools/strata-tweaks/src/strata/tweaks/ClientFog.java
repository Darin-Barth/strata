package strata.tweaks;

import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodType;

/**
 * The fog distance a client script wants this frame (kubejs/startup_scripts/hollow_fog.js sets it from the
 * RenderFog event), applied by FogRendererMixin at the very end of FogRenderer.setupFog. Distant Horizons,
 * Sodium Extra and Atmospherics all rewrite the fog distance after that event, so a value set in the event
 * alone never reaches the screen. RenderSystem is looked up by name: this mod is compiled against the server.
 */
public final class ClientFog {
    private static volatile float far = -1f;
    private static volatile float red = -1f, green, blue;
    private static MethodHandle setStart, setEnd, clearColor;
    private static boolean broken;

    private ClientFog() {}

    /** A fog end distance in blocks, or anything <= 0 to leave the game's fog alone. */
    public static void set(float blocks) {
        far = blocks;
    }

    /** The fog colour (0-1 each) for the background behind the fog, or red < 0 to leave it alone. */
    public static void setColor(float r, float g, float b) {
        green = g;
        blue = b;
        red = r;
    }

    /** The wanted fog colour, or null. */
    public static float[] color() {
        float r = red;
        return r < 0f ? null : new float[] {r, green, blue};
    }

    /** Atmospherics repaints the background with its own biome colour after the game's fog colour event. */
    public static void applyColor() {
        float r = red;
        if (r < 0f || broken) return;
        try {
            if (clearColor == null) {
                clearColor = MethodHandles.publicLookup().findStatic(Class.forName("com.mojang.blaze3d.systems.RenderSystem"),
                        "clearColor", MethodType.methodType(void.class, float.class, float.class, float.class, float.class));
            }
            clearColor.invokeExact(r, green, blue, 0f);
        } catch (Throwable t) {
            broken = true;
        }
    }

    public static void apply() {
        float end = far;
        if (end <= 0f || broken) return;
        try {
            if (setStart == null) {
                Class<?> rs = Class.forName("com.mojang.blaze3d.systems.RenderSystem");
                MethodType type = MethodType.methodType(void.class, float.class);
                setEnd = MethodHandles.publicLookup().findStatic(rs, "setShaderFogEnd", type);
                setStart = MethodHandles.publicLookup().findStatic(rs, "setShaderFogStart", type);
            }
            setStart.invokeExact(end * 0.1f);
            setEnd.invokeExact(end);
        } catch (Throwable t) {
            broken = true;
        }
    }
}
