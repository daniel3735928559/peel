DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "$DIR"
mc launch -node mu -id guppy -env '{"MU_WS_PORT":"6001","MU_ROOT_DIR":"'"$DIR"'","MU_HTTP_PORT":"6002","MU_IF":"'"$DIR"'/guppy.yaml"}'
