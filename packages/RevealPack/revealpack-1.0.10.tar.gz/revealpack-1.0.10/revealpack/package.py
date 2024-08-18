import os
import shutil
import argparse
import subprocess
import sys
import logging
import json
from _utils.config_operations import read_config, initialize_logging
from _utils.string_operations import sanitize_name

def create_package_json(config, dest_dir):
    package_info = config['info']
    package_json = {
        "name": package_info.get('short_title','title'),
        "version": package_info.get('version','1.0.0'),
        "description": package_info.get('project_title',''),
        "main": "main.js",
        "scripts": {
            "start": "electron .",
            "package-win": f"electron-packager . {package_info.get('short_title','title')} --overwrite --platform=win32 --arch=x64 --icon=assets/icons/win/icon.ico --prune=true --out=release-builds && npm run make-installer-win",
            "package-mac": f"electron-packager . {package_info.get('short_title','title')} --overwrite --platform=darwin --arch=x64 --icon=assets/icons/mac/icon.icns --prune=true --out=release-builds && npm run make-installer-mac",
            "make-installer-win": f"electron-installer-windows --src release-builds/{package_info.get('short_title','title')}-win32-x64/ --config ins-config-win.json",
            "make-installer-mac": f"electron-installer-dmg --config ins-config-mac.json release-builds/{package_info.get('short_title','title')}-darwin-x64/{package_info.get('short_title','title')}.app {package_info.get('short_title','title')} --out=release-installers",
            "test": "echo \"Error: no test specified\" && exit 1"
        },
        "keywords": [],
        "author": ", ".join(package_info['authors']),
        "license": "ISC",
        "devDependencies": {
            "electron": "^31.0.2",
            "electron-packager": "^18.3.3",
            "electron-installer-windows": "^3.0.0",
            "electron-installer-dmg": "^4.0.0"
        }
    }
    package_json_path = os.path.join(dest_dir, 'package.json')
    with open(package_json_path, 'w') as f:
        json.dump(package_json, f, indent=2)
    logging.info(f"Created package.json at {package_json_path}")

def create_ins_config_mac(config, dest_dir):
    package_info = config['info']
    ins_config_mac = {
        "title": package_info.get('short_title','title'),
        "icon": "assets/icons/mac/icon.icns",
        "overwrite": True,
        "contents": [
            {
                "x": 448,
                "y": 344,
                "type": "link",
                "path": "/Applications"
            },
            {
                "x": 192,
                "y": 344,
                "type": "file",
                "path": f"release-builds/{package_info.get('short_title','title')}-darwin-x64/{package_info.get('short_title','title')}.app"
            }
        ],
        "format": "ULFO",
        "window": {
            "size": {
                "width": 660,
                "height": 400
            }
        }
    }
    ins_config_mac_path = os.path.join(dest_dir, 'ins-config-mac.json')
    with open(ins_config_mac_path, 'w') as f:
        json.dump(ins_config_mac, f, indent=2)
    logging.info(f"Created ins-config-mac.json at {ins_config_mac_path}")

def create_ins_config_win(config, dest_dir):
    package_info = config['info']
    ins_config_win = {
        "productName": package_info.get('short_title','title'),
        "productDescription": package_info.get('project_title',''),
        "version": package_info.get('version','1.0.0'),
        "authors": ", ".join(package_info['authors']),
        "exe": f"{package_info.get('short_title','title')}.exe",
        "setupIcon": "assets/icons/win/icon.ico",
        "noMsi": True,
        "dest": "release-installers/",
        "setupExe": f"{package_info.get('short_title','title')}Installer.exe",
        "noShortcut": False,
        "runAfterFinish": False
    }
    ins_config_win_path = os.path.join(dest_dir, 'ins-config-win.json')
    with open(ins_config_win_path, 'w') as f:
        json.dump(ins_config_win, f, indent=2)
    logging.info(f"Created ins-config-win.json at {ins_config_win_path}")

def create_gitignore(dest_dir):
    gitignore_content = """# Node.js dependencies
node_modules/
npm-debug.log
yarn-error.log
package-lock.json
yarn.lock

# Logs
*.log
logs
*.log.*
logs/

# OS generated files
.DS_Store
Thumbs.db
ehthumbs.db
Desktop.ini

# Build directories
/dist
/out
/release-builds
/release-installers

# Temporary files
tmp/
temp/

# System files
*.swp
*.swo
*~
# Windows system files
$RECYCLE.BIN/
*.bak
*.ini
*.lnk
*.tmp
*.log
*.gid
*.dmp
*.mdmp
*.ldf
*.sdf

# Compiled binary addons (https://nodejs.org/api/addons.html)
build/Release

# Coverage directory used by tools like istanbul
coverage/

# NPM cache directory
.npm

# Grunt intermediate storage (https://gruntjs.com/creating-plugins#storing-task-files)
.grunt

# Bower dependency directory (https://bower.io/)
bower_components/

# NuGet packages
*.nupkg
*.snupkg

# VS Code directories
.vscode/

# SASS and other preprocessor cache
.sass-cache/
.ruby-sass-cache/

# lock files
*.lock
"""
    gitignore_path = os.path.join(dest_dir, '.gitignore')
    with open(gitignore_path, 'w') as f:
        f.write(gitignore_content)
    logging.info(f"Created .gitignore at {gitignore_path}")

def create_github_workflow(config, dest_dir):
    package_name = sanitize_name(config['info'].get('short_title','project_name'))
    workflow_content = f"""name: Build and Release Electron App

on:
  push:
    tags:
      - "v*"

jobs:
  setup-release:
    runs-on: ubuntu-latest
    outputs:
      upload_url: ${{{{ steps.create_release.outputs.upload_url }}}}
    steps:
      - uses: actions/checkout@v4
      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{{{ secrets.PERSONAL_TOKEN }}}}
        with:
          tag_name: ${{{{ github.ref }}}}
          release_name: Release ${{{{ github.ref_name }}}}
          draft: false
          prerelease: false

  build-mac:
    needs: setup-release
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20.12.2"
      - name: Install dependencies
        run: npm install
      - name: Build and package macOS
        run: npm run package-mac
      - name: List output in release-installers
        run: ls -l release-installers/
      - name: Upload macOS Installer
        uses: actions/upload-release-asset@v1.0.2
        env:
          GITHUB_TOKEN: ${{{{ secrets.PERSONAL_TOKEN }}}}
        with:
          upload_url: ${{{{ needs.setup-release.outputs.upload_url }}}}
          asset_path: ./release-installers/{package_name}.dmg
          asset_name: {package_name}.dmg
          asset_content_type: application/octet-stream

  build-win:
    needs: setup-release
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20.12.2"
      - name: Install dependencies
        run: npm install
      - name: Extract package version
        run: |
          $version = (Get-Content package.json -Raw | ConvertFrom-Json).version
          echo "VERSION=$version" >> $env:GITHUB_ENV
        shell: pwsh
      - name: Print extracted version
        run: echo "Extracted version is ${{{{ env.VERSION }}"}}
        shell: pwsh
      - name: Build and package Windows
        run: npm run package-win
      - name: List output in release-installers
        run: dir release-installers
      - name: Upload Windows Installer
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{{{ secrets.PERSONAL_TOKEN }}}}
        with:
          upload_url: ${{{{ needs.setup-release.outputs.upload_url }}}}
          asset_path: ./release-installers/{package_name}-${{{{ env.VERSION }}}}-setup.exe
          asset_name: {package_name}-${{{{ env.VERSION }}}}-setup.exe
          asset_content_type: application/vnd.microsoft.portable-executable
"""
    workflow_path = os.path.join(dest_dir, '.github', 'workflows', 'build-and-release.yml')
    os.makedirs(os.path.dirname(workflow_path), exist_ok=True)
    with open(workflow_path, 'w') as f:
        f.write(workflow_content)
    logging.info(f"Created GitHub workflow file at {workflow_path}")


def main():
    parser = argparse.ArgumentParser(description='Package Reveal.js presentations into a distributable format.')
    parser.add_argument('-r', '--root', type=str, default=os.getcwd(), help='Root directory for packaging')
    parser.add_argument('-t', '--target-dir', type=str, default=None, help='Directory to create the package')
    parser.add_argument('-n', '--no-build', action='store_true', help='Skip the build step')
    parser.add_argument('-c', '--clean', action='store_true', help='Perform a clean build before packaging')
    parser.add_argument('-d', '--decks', type=str, help='Specify decks to build (comma-separated values or a file path)')
    args = parser.parse_args()

    # Load config and initialize logging
    config = read_config(args.root)
    initialize_logging(config)

    # Handle target-dir
    if args.target_dir is None:
        args.target_dir = config["directories"].get("package", os.path.join(args.root, 'target'))
    
    if not os.path.exists(args.target_dir):
        os.makedirs(args.target_dir,exist_ok=True)
        logging.info(f"Created target directory: {args.target_dir}")
    else:
        logging.info(f"Using existing target directory: {args.target_dir}")

    # Run build step if not skipped
    if not args.no_build:
        build_script = os.path.join(os.path.dirname(__file__), 'build.py')
        python_executable = sys.executable
        build_cmd = [python_executable, build_script, '--root', args.root]
        
        if args.clean:
            build_cmd.append('--clean')
        
        if args.decks:
            build_cmd.extend(['--decks', args.decks])

        try:
            subprocess.run(build_cmd, check=True)
            logging.info("Build completed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"An error occurred during build: {e}")
            sys.exit(1)

    # Copy the build output to the target directory
    build_src_dir = config["directories"]["build"]
    target_src_dir = os.path.join(args.target_dir, 'src')

    if os.path.exists(target_src_dir):
        shutil.rmtree(target_src_dir)
        logging.info(f"Removed existing directory: {target_src_dir}")
    
    shutil.copytree(build_src_dir, target_src_dir)
    logging.info(f"Copied {build_src_dir} to {target_src_dir}")

    # Create necessary package files
    create_package_json(config, args.target_dir)
    create_ins_config_mac(config, args.target_dir)
    create_ins_config_win(config, args.target_dir)
    create_gitignore(args.target_dir)
    create_github_workflow(config, args.target_dir)

if __name__ == "__main__":
    main()
