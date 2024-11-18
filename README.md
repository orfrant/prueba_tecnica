# Prueba Técnica

El archivo con el resultado esta dentro de: **data/resultado**

Al ejecutar los scripts en cualquiera de los tres escenarios planteados el resultado se sube de forma automatica a un s3 de aws.

Para poder ser ejecutados los scripts se deben exportar las variables de entorno de aws.

Para el problema propuesto, se realizaron tres soluciones tomando los siguientes escenarios:

1. Ejecución del script en **AWS Glue**.
2. Ejecución local.
3. Ejecución en un clúster dentro de un entorno de **Kubernetes**.

## Solución 1
Esta solución es la más adecuada si se desea utilizar **AWS Glue**, ya que, utilizando la imagen de Docker oficial de AWS Glue, se tiene acceso nativo a otros servicios de AWS, como **S3**, **AWS Glue Data Catalog**, y su despliegue en un ciclo de **CI/CD**. Con esta solución, implementar un pipeline dentro de AWS sería de la siguiente forma:

1. **GitHub Actions**: Los pasos programados en Actions serían:
   - Descargar el código.
   - Ejecutar pruebas dentro del contenedor oficial de AWS Glue.
   - Subir el script a un **S3**.
   - Actualizar el job de AWS Glue.
   - Ejecutar el job (opcional), ya sea utilizando **Airflow/AWS MWAA** o desde el mismo script de Actions.

2. **AWS CodePipeline**: Serían los mismos pasos, pero con la ventaja de que maneja de forma nativa los logs con **AWS CloudWatch**.

Con esta solución y en este contexto, todo el ciclo de **CI/CD** se podría realizar dentro de **GitHub Actions** o **AWS CodePipeline**.

---

## Solución 3
Para esta solución, en la que utilizamos **Spark** dentro de un clúster de **Kubernetes (EKS)**, el pipeline puede ser un poco más complejo, pero se pueden gestionar mejor los entornos de prueba y producción. Esto se podría resolver con las siguientes tecnologías:

1. **GitHub / AWS CodePipeline**: Lo utilizaríamos para detectar la actualización del código de un job, con la diferencia de que se crearía un contenedor (con las dependencias) y se subiría a algún registro, para luego ser desplegado dentro del clúster.
2. **ECR / Docker Hub**: Se puede utilizar **ECR** como registro de contenedores o **Docker Hub**, dependiendo de las necesidades.
3. **ArgoCD**: Se utilizaría para el despliegue automático del contenedor dentro del clúster, además tiene la ventaja de que mantiene versiones de la infraestructura.
4. **Ejecución del job**: En este contexto, se puede utilizar **Airflow**, pero también se podría aprovechar el control que se tiene sobre los componentes de infraestructura y utilizar **Argo Workflows** para levantar el clúster de Spark solo mientras se ejecuta el job, lo que nos daria la ventaja de que podriamos levantar un entorno parecido a **AWS Glue** pero el cobro se haria solo sobre el uso de los nodos **EC2** y no sobre **DPU por hora**, lo cual, en ciertos contextos podria ahorrar en consumo de servicios aws.
