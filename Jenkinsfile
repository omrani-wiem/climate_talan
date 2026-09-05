pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        COMPOSE_PROJECT_NAME = 'typhoon-ci'
    }

    stages {
        stage('Checkout Git') {
            steps {
                checkout scm
            }
        }

        stage('Backend tests') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$PWD/backend:/workspace/backend" \
                      -w /workspace \
                      python:3.12-slim \
                      sh -c "pip install --quiet -r backend/requirements.txt && python -m pytest -q"
                '''
            }
        }

        stage('Frontend build') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$PWD/frontend:/workspace/frontend" \
                      -w /workspace/frontend \
                      node:20-alpine \
                      sh -c "npm ci && npm run build"
                '''
            }
        }

        stage('Docker Compose build') {
            steps {
                sh 'docker compose -f docker-compose.yml config --quiet'
                sh 'docker compose -f docker-compose.yml build'
            }
        }
    }

    post {
        always {
            sh 'docker compose -f docker-compose.yml down --remove-orphans || true'
            deleteDir()
        }
    }
}
