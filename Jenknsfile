pipeline {

    agent any

    environment {

        IMAGE_NAME = "flask-app"

    }

    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }

        }

        stage('Build Docker Image') {

            steps {

                script {

                    sh '''
                    docker build -t ${IMAGE_NAME}:${BRANCH_NAME} .
                    '''

                }
            }
        }

        stage('Deploy') {

            steps {

                script {

                    if (env.BRANCH_NAME == "main") {

                        sh '''

                        docker rm -f prod-app || true

                        docker run -d \
                        --name prod-app \
                        -p 80:5000 \
                        -e ENVIRONMENT=PRODUCTION \
                        flask-app:main

                        '''

                    }

                    else if (env.BRANCH_NAME == "dev") {

                        sh '''

                        docker rm -f dev-app || true

                        docker run -d \
                        --name dev-app \
                        -p 8081:5000 \
                        -e ENVIRONMENT=DEVELOPMENT \
                        flask-app:dev

                        '''

                    }

                    else if (env.BRANCH_NAME == "test") {

                        sh '''

                        docker rm -f test-app || true

                        docker run -d \
                        --name test-app \
                        -p 8082:5000 \
                        -e ENVIRONMENT=TESTING \
                        flask-app:test

                        '''
                    }
                }
            }
        }

    }
}

