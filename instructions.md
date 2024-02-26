(base) guobuzai@10-18-211-59 kafka-plaintext % helm install kafka-plaintext . -f values.yaml
NAME: kafka-plaintext
LAST DEPLOYED: Mon Feb 26 10:37:34 2024
NAMESPACE: fenton-neuroscience
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kafka
CHART VERSION: 26.8.5
APP VERSION: 3.6.1
---------------------------------------------------------------------------------------------
 WARNING

    By specifying "serviceType=LoadBalancer" and not configuring the authentication
    you have most likely exposed the Kafka service externally without any
    authentication mechanism.

    For security reasons, we strongly suggest that you switch to "ClusterIP" or
    "NodePort". As alternative, you can also configure the Kafka authentication.

---------------------------------------------------------------------------------------------

** Please be patient while the chart is being deployed **

Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

    kafka-plaintext.fenton-neuroscience.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    kafka-plaintext-controller-0.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9092
    kafka-plaintext-controller-1.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9092
    kafka-plaintext-controller-2.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9092

To create a pod that you can use as a Kafka client run the following commands:

    kubectl run kafka-plaintext-client --restart='Never' --image docker.io/bitnami/kafka:3.6.1-debian-11-r6 --namespace fenton-neuroscience --command -- sleep infinity
    kubectl exec --tty -i kafka-plaintext-client --namespace fenton-neuroscience -- bash

    PRODUCER:
        kafka-console-producer.sh             --broker-list kafka-plaintext-controller-0.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9092,kafka-plaintext-controller-1.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9092,kafka-plaintext-controller-2.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9092             --topic test

    CONSUMER:
        kafka-console-consumer.sh             --bootstrap-server kafka-plaintext.fenton-neuroscience.svc.cluster.local:9092             --topic test             --from-beginning
To connect to your Kafka controller+broker nodes from outside the cluster, follow these instructions:
    Kafka brokers domain: You can get the external node IP from the Kafka configuration file with the following commands (Check the EXTERNAL listener)

        1. Obtain the pod name:

        kubectl get pods --namespace fenton-neuroscience -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=kafka-plaintext,app.kubernetes.io/component=kafka"

        2. Obtain pod configuration:

        kubectl exec -it KAFKA_POD -- cat /opt/bitnami/kafka/config/server.properties | grep advertised.listeners
    Kafka brokers port: You will have a different node port for each Kafka broker. You can get the list of configured node ports using the command below:

        echo  "$(kubectl get svc --namespace fenton-neuroscience -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=kafka-plaintext,app.kubernetes.io/component=kafka,pod" -o jsonpath='{.items[*].spec.ports[0].nodePort}' | tr ' ' '\n')"
        results :   31183
                    30347
                    30728"
  
  kafka-plaintext % kubectl exec -it kafka-plaintext-controller-0 -- cat /opt/bitnami/kafka/config/server.properties | grep advertised.listeners
  
  
    advertised.listeners=CLIENT://kafka-plaintext-controller-0.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9092,INTERNAL://kafka-plaintext-controller-0.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9094,EXTERNAL://10.33.69.8:31183
    
    advertised.listeners=CLIENT://kafka-plaintext-controller-1.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9092,INTERNAL://kafka-plaintext-controller-1.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9094,EXTERNAL://10.32.250.16:30347

    advertised.listeners=CLIENT://kafka-plaintext-controller-2.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9092,INTERNAL://kafka-plaintext-controller-2.kafka-plaintext-controller-headless.fenton-neuroscience.svc.cluster.local:9094,EXTERNAL://10.32.250.21:30728
