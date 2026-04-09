pipeline {
    agent any

    environment {
        PROJECT_KEY    = 'student2-vuln-demo'
        PROJECT_NAME   = 'student2-vuln-demo'
        IMAGE_NAME     = 'student2-vuln-demo'
        CONTAINER_NAME = 'student2-vuln-demo'
        APP_PORT       = '3006'
        SONAR_HOST_URL = 'http://192.168.119.129:9000'
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
                sh 'pip3 install  --break-system-packages -r requirements.txt'
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

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
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
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished successfully.'
        }
        failure {
            echo 'Pipeline failed. Review SonarQube and Jenkins logs.'
        }
    }
}
