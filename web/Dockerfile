From zxinxin/bludit:3.9.2-base
RUN yum -y install openssh-server

RUN mkdir /var/run/sshd
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
RUN ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ''
RUN ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N ''
RUN ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ''

RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config    
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN /bin/echo 'root:admin'|chpasswd
RUN /bin/sed -i 's/.session.required.pam_loginuid.so./session optional pam_loginuid.so/g' /etc/pam.d/sshd
RUN /bin/echo -e "LANG="en_US.UTF-8"" > /etc/default/local

EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]