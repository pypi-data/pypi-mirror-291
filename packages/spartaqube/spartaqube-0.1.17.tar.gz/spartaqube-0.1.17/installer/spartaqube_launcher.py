import os, sys, site, subprocess, argparse

def get_spartaqube_path():
    '''
    Get spartaqube path within site-packages
    '''
    site_packages_dir = site.getsitepackages()
    site_packages_path = [elem for elem in site_packages_dir if 'site-packages' in elem][0]
    return os.path.join(site_packages_path, 'spartaqube')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SpartaQube Launcher Script')
    parser.add_argument('--silent', action='store_true', help='Run the script in silent mode')
    parser.add_argument('--port', type=int, help='Port to use for the service', default=None)
    # Parse the arguments
    args = parser.parse_args()

    b_open_browser = True
    port = args.port
    if len(sys.argv) > 1:
        args = sys.argv[1:]

    base_path = get_spartaqube_path()
    # api_folder = os.path.join(base_path, 'api')
    sys.path.insert(0, base_path)
    from spartaqube.api import spartaqube_install
    spartaqube_install.entrypoint(port=port, b_open_browser=b_open_browser)

    # process = subprocess.Popen("python spartaqube_install.py", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=api_folder, universal_newlines=True)
    # while True:
        # output = process.stdout.readline()
        # if output:
            # print(output.strip())