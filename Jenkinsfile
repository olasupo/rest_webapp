pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '5'))
    }

    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/olasupo/rest_webapp.git'
            }
        }

       stage('Run db_connector.py (Database Connection)') {
            steps {
                script {
                    sh 'python3 db_connector.py'
                }
            }
        }

        stage('Run rest_app.py (backend)') {
            steps {
                script {
                    sh 'nohup python3 rest_app.py &'
                }
            }
        }



        stage('Run backend_testing.py') {
            steps {
                script {
                    sh 'python3 backend_testing.py'
                }
            }
        }



        stage('Run clean_environment.py') {
            steps {
                script {
                    sh 'python3 clean_environment.py'
                    sh 'sudo docker stop dev_mysql'
                    sh 'sudo docker rm dev_mysql'
                }
            }
        }

        stage('Build docker image for rest_webapp') {
            steps {
                script {
                    sh 'sudo docker build -t rest_webapp .'
                }
            }
        }
         stage('Push image to Docker hub') {
            steps {
                script {
                    sh 'sudo docker push olasupoo/rest_webapp:latest'
                }
            }
        }
        stage('Run docker-compose') {
            steps {
                script {
                    sh 'sudo docker-compose up -d'
                }
            }
        }
        stage('Run docker_backend_testing.py') {
            steps {
                script {
                    sh 'python3 docker_backend_testing.py'
                }
            }
        }
        stage('Cleanup') {
            steps {
                script {
                    sh 'sudo docker-compose down'
                    sh 'sudo docker rmi rest_webapp'
                }
            }
        }
    }


}
