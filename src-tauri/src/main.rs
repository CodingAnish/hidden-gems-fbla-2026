#![cfg_attr(all(not(debug_assertions), target_os = "windows"), windows_subsystem = "windows")]

use std::process::{Child, Command};
use std::time::Duration;
use std::thread;
use std::env;
use std::sync::Mutex;
use tauri::Manager;

lazy_static::lazy_static! {
    static ref FLASK_PROCESS: Mutex<Option<Child>> = Mutex::new(None);
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

pub fn start_flask() -> Result<String, String> {
    // Check if Flask is already running by testing the port
    println!("[Tauri] Checking if Flask is already running on port 5001...");
    
    // Try to connect to Flask
    match std::net::TcpStream::connect("127.0.0.1:5001") {
        Ok(_) => {
            println!("[Tauri] Flask is already running");
            return Ok("Flask is already running".to_string());
        }
        Err(_) => {
            println!("[Tauri] Flask not running, attempting to start...");
        }
    }

    // Try to find the app root directory
    let mut app_dir = env::current_dir().map_err(|e| format!("Failed to get current dir: {}", e))?;
    
    // When running from Tauri, we might be in a different directory
    // Check if we're in src-tauri directory and go up one level
    if app_dir.ends_with("src-tauri") {
        app_dir.pop();
    }

    let python_path = if cfg!(target_os = "windows") {
        app_dir.join(".venv\\Scripts\\python.exe")
    } else {
        app_dir.join(".venv/bin/python")
    };

    if !python_path.exists() {
        // Try alternative path
        let alt_path = app_dir.join(".venv/bin/python");
        if !alt_path.exists() {
            return Err(format!("Python executable not found at {:?}", python_path));
        }
    }

    // Spawn Flask in the background
    let child = Command::new(&python_path)
        .args(&["-m", "web.app"])
        .current_dir(&app_dir)
        .spawn()
        .map_err(|e| format!("Failed to start Flask: {}", e))?;

    // Store the process
    *FLASK_PROCESS.lock().unwrap() = Some(child);

    // Wait for Flask to be ready
    println!("[Tauri] Waiting for Flask to start...");
    for i in 0..30 {
        if let Ok(_) = std::net::TcpStream::connect("127.0.0.1:5001") {
            println!("[Tauri] Flask started successfully");
            return Ok("Flask started".to_string());
        }
        if i < 29 {
            thread::sleep(Duration::from_millis(500));
        }
    }

    Err("Flask did not start in time".to_string())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .setup(|app| {
            // Try to start Flask, but don't fail if it's already running
            match start_flask() {
                Ok(msg) => println!("[Tauri Setup] {}", msg),
                Err(e) => println!("[Tauri Setup] Flask may already be running: {}", e),
            }

            // Add a small delay to ensure Flask is ready
            thread::sleep(Duration::from_millis(500));

            // Get all existing windows
            let existing_windows: Vec<String> = app.windows().keys().cloned().collect();
            
            // Only create window if 'main' doesn't already exist
            if !existing_windows.contains(&"main".to_string()) {
                tauri::WindowBuilder::new(
                    app,
                    "main",
                    tauri::WindowUrl::App("http://localhost:5001".into()),
                )
                .title("Hidden Gems")
                .inner_size(1200.0, 800.0)
                .resizable(true)
                .build()?;
            } else {
                println!("[Tauri Setup] Window 'main' already exists");
            }

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");

    // Cleanup Flask process on app exit (optional, since Flask is managed separately)
    if let Ok(mut process_lock) = FLASK_PROCESS.lock() {
        if let Some(mut child) = process_lock.take() {
            println!("[Tauri] Stopping Flask process...");
            let _ = child.kill();
        }
    }
}
