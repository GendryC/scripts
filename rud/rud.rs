use std::fs;
use std::path::Path;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: ./bin -n <name> -s <module> <service> -m <module> <model> -c <module> <controller> -e <language>");
        return;
    }

    let command = &args[1];
    let name = &args[2];

    match command.as_str() {
        "-n" => create_base_structure(name),
        "-s" => {
            if args.len() != 4 {
                eprintln!("Usage for service: ./bin -s <module> <service>");
                return;
            }
            create_service(name, &args[3]);
        },
        "-m" => {
            if args.len() != 4 {
                eprintln!("Usage for model: ./bin -m <module> <model>");
                return;
            }
            create_model(name, &args[3]);
        },
        "-c" => {
            if args.len() != 4 {
                eprintln!("Usage for controller: ./bin -c <module> <controller>");
                return;
            }
            create_controller(name, &args[3]);
        },
        "-e" => {
            if args.len() != 4 {
                eprintln!("Usage for extension change: ./bin -e <language>");
                return;
            }
            change_extension(name, &args[3]);
        },
        _ => eprintln!("Unknown command"),
    }
}

fn create_base_structure(name: &str) {
    let folders = ["controllers", "dtos", "models", "services"];
    fs::create_dir(name).unwrap();
    for folder in folders.iter() {
        let folder_path = format!("{}/{}", name, folder);
        fs::create_dir(&folder_path).unwrap();
    }
}

fn create_service(module: &str, service: &str) {
    let service_path = format!("{}/services/{}.service.rs", module, service);
    fs::write(service_path, "// Service code").unwrap();
}

fn create_model(module: &str, model: &str) {
    let model_path = format!("{}/models/{}.model.rs", module, model);
    fs::write(&model_path, "// Model code").unwrap();
    let dto_path = format!("{}/dtos/{}.dto.rs", module, model);
    fs::write(&dto_path, "// DTO code").unwrap();
}

fn create_controller(module: &str, controller: &str) {
    let controller_path = format!("{}/controllers/{}.controller.rs", module, controller);
    fs::write(controller_path, "// Controller code").unwrap();
}

fn change_extension(module: &str, language: &str) {
    let extension = match language {
        "rust" | "rs" => "rs",
        "typescript" | "ts" => "ts",
        "javascript" | "js" => "js",
        _ => "",
    };
    if extension.is_empty() {
        eprintln!("Unsupported language");
        return;
    }

    let module_path = Path::new(module);
    if module_path.exists() && module_path.is_dir() {
        change_extension_recursively(&module_path, extension);
    } else {
        eprintln!("Module path not found: {}", module);
    }
}

fn change_extension_recursively(dir: &Path, extension: &str) {
    let paths = fs::read_dir(dir).unwrap();
    for path in paths {
        let path = path.unwrap().path();
        if path.is_file() {
            let file_stem = path.file_stem().unwrap().to_str().unwrap();
            let new_path = path.with_file_name(format!("{}.{}", file_stem, extension));
            fs::rename(&path, new_path).unwrap();
        } else if path.is_dir() {
            change_extension_recursively(&path, extension);
        }
    }
}
