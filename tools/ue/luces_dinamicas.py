"""Iluminación 100 % dinámica en el mapa existente (sin luz horneada).

El juego no hornea luz (3000 instancias y 91 baldosas de terreno: lightmaps caros en una GTX 1060),
pero las luces quedaban Stationary por defecto y el motor avisaba en pantalla
"LIGHTING NEEDS TO BE REBUILT". La causa se arregla así: todas las luces Movable y, en el
proyecto, r.AllowStaticLighting=False. De paso baja el motion blur (lectura del espacio en combate).
Uso: tools/ue/correr.sh tools/ue/luces_dinamicas.py
"""
import unreal

niveles = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
actores = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
niveles.load_level("/Game/Vaelith/Mapas/Lvl_Vaelith")

cambiadas, total = 0, 0
for a in actores.get_all_level_actors():
    for lc in a.get_components_by_class(unreal.LightComponentBase):
        total += 1
        if lc.get_editor_property("mobility") != unreal.ComponentMobility.MOVABLE:
            lc.set_mobility(unreal.ComponentMobility.MOVABLE)
            cambiadas += 1
    if isinstance(a, unreal.PostProcessVolume):
        s = a.get_editor_property("settings")
        s.set_editor_property("override_motion_blur_amount", True)
        s.set_editor_property("motion_blur_amount", 0.1)
        s.set_editor_property("override_motion_blur_max", True)
        s.set_editor_property("motion_blur_max", 2.0)
        a.set_editor_property("settings", s)
        unreal.log("[vaelith] motion blur 0.1 en " + a.get_name())
unreal.log(f"[vaelith] luces: {total}, pasadas a Movable: {cambiadas}")
niveles.save_current_level()
