Hola!
-----

This is a simple app which has dynamic configuration demo and provide basic configmap, secret, iam role usage and kubernetes deployment spec.


Principals
----------

[*Codebase*](https://12factor.net/codebase): Codebase will be same for across all deployments,
however deployments can run multiple versions of the app in different environments (preprod/prod/staging/foo's local laptop/bar's staging cluster)

[*Dependencies*](https://12factor.net/dependencies): `./requirements.txt` contains all required
dependencies. This project is developed using virtual environment in local, but inside container
there is not venv

[*Config*](https://12factor.net/config): We identified configs as key-value pairs and secrets. KVs
and Secrets are being managed by ConfigMap and Secrets respectively. Confd sidecar can be used to dynamically fetch config from consul and store in a local directory which you can mount as config volume. Config change doesn't require new deployment.

[*Backing Services*](https://12factor.net/backing-services): Services must be treated as resources
and URLs and credentials must use config maps or secrets as necessary.

[*Build, release, run*](https://12factor.net/build-release-run):
  - Build is docker build phase, which
gets initialized when you push to github. Build is defined here: `./.drone.yml`
  - Release and run phases are managed by argo. Click on 'Sync' on respective argo application to
    release and rollout deploy

[*Processes*](https://12factor.net/processes): Hola app runs as gunicorn process with 4 worker processes.

[*Port binding*](https://12factor.net/port-binding): Hosts the app on 5000

[*Concurrency*](https://12factor.net/concurrency): As a twelve factor application, hola doesn't
manage any PID file and gunicorn runs as pid 0 process, so that we can easily orchestrate using
kubernetes to manage log output stream, release, scaling

[*Disposability*](https://12factor.net/disposability): Disposability is
delegated to gunicorn and supports these (signals)[http://docs.gunicorn.org/en/latest/signals.html].
However disposability is far vast topic more than just handling signals but `hola` being a simple
app there is not much to demonstrate.

[*Dev/prod parity*](https://12factor.net/dev-prod-parity): Same architecture for all
environments, mostly configmaps and secret will differ.

[*Logs*](https://12factor.net/logs): As a 12factor app, the app should never manage log files
itself and send logs as unbuffered stream to `stdout`

[*Admin processes*](https://12factor.net/admin-processes): Since we are running kubernetes, define
admin commands the app supports in `entrypoint.sh` and run them as `Job` in kubernetes.

