# Prueba Tecnica

Para el problema propuesto se realizaron tres soluciones, para los siguientes tres escenarios:

    1. Ejecucion del script en AWS Glue.
    2. Ejecucion local.
    3. Ejecucion en un cluster dentro de un entorno de kubernetes.

**Solucion 1.** Esta solucion es la mejor si se desea utilizar AWS Glue, ya que utilizando la imagen de docker oficial de aws glue tenemos acceso nativo a los otros servicios de aws, como s3, aws glue data catalog y su despliegue en un ciclo de ci/cd. con esta solucion implementar un pipeline dentro de aws seria de la siguiente forma:

    1. Github actions: Los pasos programados sobre el actions serian
        * Descargar el codigo.
        * Ejecutar pruebas dentro del contenedor oficial de aws glue.
        * Subir el script a un S3.
        * Actualizar el job de aws glue.
        * Ejecutar el job (opcional), utilizando ya sea Airflow o desde el mismo script de actions.

    2. AWS Code Pipeline: Serian los mismos pasos pero con la ventaja que maneja de forma nativa los logs con AWS CloudWatch.

Con esta solucion y en este contexto, todo el ciclo de ci/cd se podria hacer dentro de github actions o AWS Code Pipeline.


**Solucion 3.** Para esta solucion en donde utilizamos spark dentro de un cluster de kubernetes (EKS), el pipeline puede ser un poco mas complejo, pero podriamos manejar de mejor forma ambientes de prueba y produccion y podria resolverse con las siguientes tecnologias.

    1. Github / AWS Codepipeline: lo usariamos para detectar la actualizacion del codigo de un job, con la diferencia que se crearia un contenedor (con las dependencias) y se subiria a algun registro, para luego ser desplegado dentro del cluster.
    3. ECR / Docker hub: Se puede utilizar ECR como registro de contenedores o docker hub, dependiendo de las necesidades.
    4. ArgoCd: Se utilizaria para el despliegue del contenedor dentro de nuestro cluster de forma automatica, y ademas tiene la ventaja que mantiene versiones de la infraestructura.
    5. Ejecutar el job, bajo este contexto se puede utilizar airflow, pero tambien se podria aprovechar que se tiene control de los componentes de infraestructura y utilizar ArgoWorkflows, para levantar el cluster de spark solo mientras se ejecuta el job. 
