#!/bin/sh

# Discord RPC
for i in {0..9}; do
    test -S $XDG_RUNTIME_DIR/discord-ipc-$i || ln -sf {app/com.discordapp.Discord,$XDG_RUNTIME_DIR}/discord-ipc-$i;
done

# Change references to old flatpak data dir in config file to new data dir
sed -i s/moe.launcher.an-anime-game-launcher-gtk/moe.launcher.an-anime-game-launcher/ $XDG_DATA_HOME/anime-game-launcher/config.json

# Modify /etc/hosts to block logging servers
# This is possible because /etc is a writable tmpfs in flatpak
if readlink /etc/hosts > /dev/null; then
    # /etc/hosts is a symlink by default, if it is, copy the original and modify it
    # Otherwise, we already modified it
    original=$(readlink /etc/hosts)
    rm /etc/hosts
    cp $original /etc/hosts
    cat <<EOF >> /etc/hosts
# Global
# Genshin logging servers (do not remove!)
0.0.0.0 overseauspider.yuanshen.com
0.0.0.0 log-upload-os.hoyoverse.com
0.0.0.0 log-upload-os.mihoyo.com
0.0.0.0 sg-public-data-api.hoyoverse.com

# China
# Genshin logging servers (do not remove!)
0.0.0.0 log-upload.mihoyo.com
0.0.0.0 uspider.yuanshen.com
0.0.0.0 public-data-api.mihoyo.com
EOF

    # If NO_BLOCK_PROXY is set, don't block the proxy/cdn servers
    if [ -z "$NO_BLOCK_PROXY" ]; then
        cat <<EOF >> /etc/hosts
# Optional Unity proxy/cdn servers
0.0.0.0 prd-lender.cdp.internal.unity3d.com
0.0.0.0 thind-prd-knob.data.ie.unity3d.com
0.0.0.0 thind-gke-usc.prd.data.corp.unity3d.com
0.0.0.0 cdp.cloud.unity3d.com
0.0.0.0 remote-config-proxy-prd.uca.cloud.unity3d.com
EOF
    fi
fi

export PATH=$PATH:/usr/lib/extensions/vulkan/gamescope/bin

exec anime-game-launcher "$@"
