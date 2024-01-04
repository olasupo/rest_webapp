pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '5'))
    }

    triggers {
        pollSCM('* * * * *')
    }

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('olasupoo') 
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
                    sh 'docker stop dev_mysql'
                    sh 'docker rm dev_mysql'
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

        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'olasupoo', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u $DOCKER_USER -p $DOCKER_PASSWORD"
                    }
                }
            }
        }

        stage('Push image to Docker hub') {
            steps {
                script {
                    sh 'docker tag rest_webapp olasupoo/rest_webapp:latest'
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

