pipeline {
    agent any

    environment {
        PROJECT_KEY    = 'student2-owsap'
        PROJECT_NAME   = 'student2-owsap'
        IMAGE_NAME     = 'student2-owsap'
        CONTAINER_NAME = 'student2-owsap'
        APP_PORT       = '3011'
        SONAR_HOST_URL = 'http://192.168.119.129:9000'
        APP_URL        = 'http://localhost:3010'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Checkout') {
            steps {
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            sonar-scanner \
                            -Dsonar.projectKey=$PROJECT_KEY \
                            -Dsonar.projectName=$PROJECT_NAME \
                            -Dsonar.projectVersion=1.0 \
                            -Dsonar.sources=. \
                            -Dsonar.inclusions=**/*.py \
                            -Dsonar.sourceEncoding=UTF-8 \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Run App') {
            steps {
                sh 'docker rm -f ${CONTAINER_NAME} || true'
                sh 'docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:3000 ${IMAGE_NAME}:latest'
                sh 'sleep 10'
                sh 'curl -I ${APP_URL} || true'
            }
        }

        stage('OWASP ZAP Scan') {
            steps {
                sh '''
                    mkdir -p zap-report

                    docker run --rm --network host \
                      -v $(pwd)/zap-report:/zap/wrk/:rw \
                      ghcr.io/zaproxy/zaproxy:stable \
                      zap-baseline.py \
                      -t ${APP_URL} \
                      -r zap-report.html \
                      -J zap-report.json \
                      -m 3 || true
                '''
            }
        }

        stage('Fail on ZAP High Alerts') {
            steps {
                sh '''
                    python3 - << 'PY'
import json
import sys

report_file = 'zap-report/zap-report.json'

with open(report_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

high_count = 0
medium_count = 0

site = data.get('site')
if isinstance(site, list):
    sites = site
else:
    sites = [site] if site else []

for s in sites:
    for alert in s.get('alerts', []):
        risk = str(alert.get('riskcode', '0'))
        if risk == '3':
            high_count += 1
        elif risk == '2':
            medium_count += 1

print(f"HIGH alerts: {high_count}")
print(f"MEDIUM alerts: {medium_count}")

if high_count > 0:
    sys.exit(1)
PY
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'zap-report/*', fingerprint: true, allowEmptyArchive: true
        }
        success {
            echo 'Pipeline finished successfully.'
        }
        failure {
            echo 'Pipeline failed. Review ZAP report and Jenkins logs.'
        }
    }
}
