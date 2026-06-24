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

        stage('Monitoring Stack') {
            when { branch 'main' }   // run monitoring only in prod
            steps {
                sh """
                docker compose -f monitoring/docker-compose.yml up -d
                """
                echo "Prometheus and Grafana deployed on EC2"
            }
        }

        stage('Verify Prometheus') {
            when { branch 'main' }
            steps {
                sh '''
                for i in {1..60}; do
                  if curl -s http://localhost:9090/-/ready; then
                    echo "Prometheus is ready"
                    exit 0
                  fi
                  echo "Waiting for Prometheus..."
                  sleep 5
                done
                echo "Prometheus not ready after 5 minutes"
                exit 1
                '''
            }
        }

        stage('Verify Grafana') {
            when { branch 'main' }
            steps {
                sh '''
                for i in {1..30}; do
                  if [ "$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/login)" -eq 200 ]; then
                    echo "Grafana is ready"
                    exit 0
                  fi
                  echo "Waiting for Grafana..."
                  sleep 5
                done
                echo "Grafana not ready after 150s"
                exit 1
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished for branch: ${env.BRANCH_NAME}"
        }
    }
}
