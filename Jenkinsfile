pipeline {
    agent { label 'vinod' }

    environment {
        IMAGE_NAME = "flask-app"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Branch detected: ${env.BRANCH_NAME}"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${env.BRANCH_NAME} .
                """
                echo "Docker image built successfully for ${env.BRANCH_NAME}"
            }
        }

        stage('Deploy to Dev') {
            when { branch 'dev' }
            steps {
                sh """
                docker rm -f dev-app || true
                docker run -d \
                  --name dev-app \
                  -p 8081:5000 \
                  -e ENVIRONMENT=DEVELOPMENT \
                  ${IMAGE_NAME}:dev
                """
            }
        }

        stage('Deploy to Test') {
            when { branch 'test' }
            steps {
                sh """
                docker rm -f test-app || true
                docker run -d \
                  --name test-app \
                  -p 8082:5000 \
                  -e ENVIRONMENT=TESTING \
                  ${IMAGE_NAME}:test
                """
            }
        }

        stage('Deploy to Prod') {
            when { branch 'main' }
            steps {
                sh """
                docker rm -f prod-app || true
                docker run -d \
                  --name prod-app \
                  -p 80:5000 \
                  -e ENVIRONMENT=PRODUCTION \
                  ${IMAGE_NAME}:main
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline finished for branch: ${env.BRANCH_NAME}"
        }
    }
}
