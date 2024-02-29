TO CREATE AUTH BETWEEN PROXY AND CLIENT:
replae username with the actual username you want to specify. 

htpasswd -c auth username

When prompted, enter and confirm your password.
Next, create a Kubernetes Secret in the fenton-neuroscience namespace from this file:


kubectl create secret generic basic-auth --from-file=auth -n fenton-neuroscience

