import json

import enums
import project

def mcmeta_from_lmproj(proj: project.LimboProject) -> str:
    meta = {
        "pack": {
            "pack_format": enums.pack_format_map.get(proj.minecraft_version),
            "description": f"&7&k# &rGenerated With &3&lLimbo &7&k#\n"
                           f"#&r&f {proj.name} &7version &a{proj.version} &7&k#"
        }
    }

    return json.dumps(meta, indent=1).replace("&", "§")
