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
                git 'https://github.com/olasupo/Project_Part1.git'
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
                }
            }
        }

        stage('Build docker image for rest_webapp') {
            steps {
                script {
                    sh 'docker build -t rest_webapp .'
                }
            }
        }
         stage('Push image to Docker hub') {
            steps {
                script {
                    sh 'docker push olasupoo/rest_webapp:latest'
                }
            }
        }
        stage('Run docker-compose') {
            steps {
                script {
                    sh 'docker-compose up -d'
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
                    sh 'docker-compose down'
                    sh 'docker rmi rest_webapp'
                }
            }
        }
    }


}
