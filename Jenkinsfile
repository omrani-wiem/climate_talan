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
                sh 'python3 -m venv .ci-venv'
                sh '.ci-venv/bin/pip install --quiet -r backend/requirements.txt'
                sh '.ci-venv/bin/python -m pytest -q'
            }
        }

        stage('Frontend build') {
            steps {
                dir('frontend') {
                    sh 'npm ci'
                    sh 'npm run build'
                }
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
