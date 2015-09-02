#!/usr/bin/env bash

set -e
set -o pipefail

cd "$(dirname "$0")"

# Add the 'ubuntu' user if it does not already exist
if [ -z "$(cat /etc/passwd | grep '^ubuntu:')" ]; then
  useradd -m --shell /bin/bash ubuntu
fi

# Give the ubuntu user sudo privileges without a password
if [ ! -e /etc/sudoers.d/ubuntu ]; then
  echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ubuntu
  chmod 440 /etc/sudoers.d/ubuntu
fi

# Generate a keypair the ubuntu user
if [ ! -f /home/ubuntu/.ssh/id_rsa ]; then
  su ubuntu -c 'mkdir -p ~/.ssh && ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa'
fi

if [ ! -z "$LOCAL_SSH_KEY" ]; then
  if grep -Fxq "$LOCAL_SSH_KEY" /home/ubuntu/.ssh/authorized_keys; then
    echo 'Local SSH public key already in remote authorized_keys'
  else
    echo 'Adding local SSH public key to authorized_keys'
    echo "$LOCAL_SSH_KEY" >> /home/ubuntu/.ssh/authorized_keys
    echo 'Key successfully added. You should now be able to SSH to this host as ubuntu@host'
  fi
fi

# SSH permissions
chown -R ubuntu:ubuntu /home/ubuntu/.ssh
chmod -R 600 /home/ubuntu/.ssh
chmod +x /home/ubuntu/.ssh

# Disable root access
passwd -l root
echo 'SSH access for root disabled. You will need to connect as ubuntu.'
