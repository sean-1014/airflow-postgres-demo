# Airflow Postgres Demo

This demo shows how one would use Airflow to copy data from one Postgres database to another. Docker containers are used to represent services in a production environment. 

## Setup
The `docker-compose.yaml` describes the service definitions. Most of it is adapted from the official Airflow [docker-compose](https://airflow.apache.org/docs/apache-airflow/2.3.2/docker-compose.yaml), with some minor tweaks, mainly the use of the `LocalExecutor` instead of the `CeleryExecutor` to reduce overhead since this is a toy application. For more information about the Airflow-provided `docker-compose`, see [this page](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).

To set up the test environment, first run the startup script `startup.sh` if running from Linux. This creates three directories Airflow is going to use as volumes as specified in the `docker-compose` file and set the Airflow UID to the UID your user account is using.

### Initializing Environment
```console
you@host:$ docker-compose up airflow-init
```

### Running Airflow
```console
you@host:$ docker-compose up
```

### Cleaning Up
```console
you@host:$ docker-compose down --volumes --remove-orphans
```

## Services
### Airflow Components
- `postgres`: Airflow metadata server
- `airflow-webserver`: Airflow webserver. Accessible at `localhost:5884`. Web UI login credentials: `user: airflow; password: airflow`
- `airflow-scheduler`: Airflow scheduler
- `airflow-init`: Performs some checks and initializes Airflow
- `airflow-cli`: Airflow CLI

### Toy Database Components
- `postgres-source`: Login credentials: `user: postgres; password: postgres`
- `postgres-target`: Login credentials: `user: postgres; password: postgres`
- `pg-admin`: Web-based frontend for inspecting the databases. Accessible at `localhost:5050`. Login credentials: `email: admin@admin.com; password: root`

## Demonstration
The demonstration can be found in `dags/postgres_dag/postgres_dag.py`. The DAG should show up automatically on the Airflow Web UI.

### Data
At startup, `postgres-source` gets populated with the `sales` table

| id  | creation_date | sale_value |
| --- | ------------- | ---------- |
|  0  |  2022-06-15   |  1234.56   |
|  1  |  2022-06-16   |  9876.54   |

You can view this in `pg-admin` by first linking to the Postgres database, then navigating to `Servers/<registered db name>/Databases/postgres/Schemas/public/Tables/sales`.

The `postgres-target` database starts off empty, but after running the DAG, the `sales` table should be copied there.