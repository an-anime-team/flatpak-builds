#!/bin/sh

# Discord RPC
for i in {0..9}; do
    test -S $XDG_RUNTIME_DIR/discord-ipc-$i || ln -sf {app/com.discordapp.Discord,$XDG_RUNTIME_DIR}/discord-ipc-$i;
done

# Modify /etc/hosts to block logging servers
# This is possible because /etc is a writable tmpfs in flatpak
if readlink /etc/hosts > /dev/null; then
    # /etc/hosts is a symlink by default, if it is, copy the original and modify it
    # Otherwise, we already modified it
    original=$(readlink /etc/hosts)
    rm /etc/hosts
    cp $original /etc/hosts
    cat <<EOF >> /etc/hosts
# TODO
EOF
fi

export PATH=$PATH:/usr/lib/extensions/vulkan/gamescope/bin

exec anime-borb-launcher "$@"
