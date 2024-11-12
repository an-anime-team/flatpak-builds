#!/bin/sh

# This is possible because /etc is a writable tmpfs in flatpak
if readlink /etc/hosts > /dev/null; then
    # /etc/hosts is a symlink by default, if it is, copy the original and modify it
    # Otherwise, we already modified it
    original=$(readlink /etc/hosts)
    rm /etc/hosts
    cp $original /etc/hosts
    cat <<EOF >> /etc/hosts
0.0.0.0 pc.crashsight.wetest.net
EOF
fi

export PATH=$PATH:/usr/lib/extensions/vulkan/gamescope/bin

exec wavey-launcher "$@"
