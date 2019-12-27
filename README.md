Proposal for adoption of 12 factor app methodology
--------------------------------------------------

This repository is just for an example of how the services would look like after dockerization.


Principals
----------

(*Codebase*)[https://12factor.net/codebase]: Codebase will be same for across all deployments,
however deployments can run multiple versions of the app in different environments (preprod/prod/staging/foo's local laptop/bar's staging cluster)

(*Dependencies*)[https://12factor.net/dependencies]: `./requirements.txt` contains all required
dependencies. This project is developed using virtual environment in local, but inside container
there is not venv

(*Config*)[https://12factor.net/config]

