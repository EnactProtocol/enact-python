import venv
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Optional
import pkg_resources


class DependencyManager:
    def __init__(self, venv_path: Optional[Path] = None):
        """Initialize dependency manager with optional custom venv path"""
        self.venv_path = venv_path or Path(tempfile.mkdtemp()) / '.venv'
        self._ensure_venv()

    def _ensure_venv(self):
        """Create virtual environment if it doesn't exist"""
        if not self.venv_path.exists():
            venv.create(self.venv_path, with_pip=True)

    def _get_pip_path(self) -> Path:
        """Get path to pip executable in venv"""
        if os.name == 'nt':  # Windows
            return self.venv_path / 'Scripts' / 'pip.exe'
        return self.venv_path / 'bin' / 'pip'

    def _get_python_path(self) -> Path:
        """Get path to Python executable in venv"""
        if os.name == 'nt':  # Windows
            return self.venv_path / 'Scripts' / 'python.exe'
        return self.venv_path / 'bin' / 'python'

    def install_dependencies(self, dependencies: Dict) -> None:
        """Install dependencies from Enact task definition"""
        if 'python' not in dependencies:
            return

        python_deps = dependencies['python']

        # Check Python version compatibility
        if 'python_version' in python_deps:
            self._check_python_version(python_deps['python_version'])

        # Install required packages
        if 'packages' in python_deps:
            requirements = [
                f"{pkg['name']}{pkg['version']}"
                for pkg in python_deps['packages']
            ]
            self._install_packages(requirements)

    def _check_python_version(self, version_spec: str) -> None:
        """Check if current Python version meets requirements"""
        current_version = pkg_resources.parse_version(
            pkg_resources.get_distribution('python').version)
        if not pkg_resources.Requirement.parse(f"python{version_spec}").contains(current_version):
            raise RuntimeError(
                f"Python version {current_version} does not meet requirement: {version_spec}")

    def _install_packages(self, requirements: List[str]) -> None:
        """Install Python packages in the virtual environment"""
        pip_path = self._get_pip_path()
        process = subprocess.run(
            [str(pip_path), 'install'] + requirements,
            capture_output=True,
            text=True
        )
        if process.returncode != 0:
            raise RuntimeError(
                f"Failed to install dependencies: {process.stderr}")

    def execute_in_venv(self, script: str) -> str:
        """Execute a script in the virtual environment"""
        python_path = self._get_python_path()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(script)
            tmp.flush()

            try:
                process = subprocess.run(
                    [str(python_path), tmp.name],
                    capture_output=True,
                    text=True
                )
                if process.returncode != 0:
                    raise RuntimeError(
                        f"Script execution failed: {process.stderr}")
                return process.stdout
            finally:
                os.unlink(tmp.name)
