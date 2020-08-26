## AWS setup step by step:

1. Created account in Amazon VPC
2. Created IAM user
3. Setup aws cli

  * ```$ aws configure```
4. Created RDS instance

  * ```
    Create new db:
    $ aws rds create-db-instance \
        --db-instance-identifier sixty \
        --db-instance-class db.t2.micro \
        --engine postgres \
        --allocated-storage 20 \
        --master-username postgres \
        --master-user-password <passwd> \
        --enable-iam-database-authentication \
        --publicly-accessible 
    ```
  * ![Database](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/DB.png)

5. Created VPC Security Groups Inbound rules to My IP
6. Setup DB

  * ```$ psql --host sixty.c9pwzjvvfbdr.eu-west-2.rds.amazonaws.com --port 5432 -U postgres --password```
  * ```
    create database sixty_db;
    create user sixty with encrypted password '<passwd>';
    grant all privileges on database sixty_db to sixty;
    ```

7. Created namespace in ECR (also docker python3.7 and alpine)
8. Docker login to AWS and push dockers

  * ```$ aws ecr get-login-password | docker login -u AWS --password-stdin 283644123497.dkr.ecr.eu-west-2.amazonaws.com```
  * ```$ docker tag <img_id> <repo_addr> && docker push <repo_addr>```
  * ![ECR](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/ECR.png)

9. Created ECS Cluster
10. Created Task definition

  * Task memory (MiB) 512 ; Task CPU (unit) 256, Requires compatibilities - FARGATE
  * Set Secure group with ports (Inbound) 5432, 80, 443 and Outbound (All)
  * Set healthcheck of docker with curl
  * ![Docker-HCH](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/Docker-HCH.png)
  
11. Created two running tasks from the same task definition (for load balancer) = testing phase

  * Pub IP: ```35.176.73.18``` and ```3.8.23.60```
12. Created service from definned task definition with 2 replicas = production phase

  * ![Cluster-prod](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/Cluster-prod.png)
13. Created ELB

  * DNS name ```web-app-lb-1617483936.eu-west-2.elb.amazonaws.com```
  * Target group with two targets IPs
  * ![Targets](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/Targets.png)
  * Listener for HTTP (80)

14. Registered own domain (```ondrejfuchs.cz```)
15. Created SSL certificate by ACM
16. Added new Listener to ELB (for 443)

  * ![Listeners](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/Listeners.png)
17. Created Alias by Route 53 from __web-app.ondrejfuchs.cz__ to DNS name of ELB
18. App available on subdomain __web-app.ondrejfuchs.cz__ (80 and 443)

  * ![HTTP_check](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/HTTP_check.png)
  * ![HTTPS_check](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/HTTPS_check.png)

19. Check task logs:
  * ![Task_logs](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/Task_logs.png)

10. Billing sumary
  * ![Billing](https://github.com/ondrejFuchs/web-app/blob/master/aws-setup/imgs/Billing.png)
