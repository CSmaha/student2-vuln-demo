pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Checkout') {
            steps {
                sh 'ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'npm install'
            }
        }

        stage('Snyk Scan') {
            steps {
                echo 'Snyk scan stage'
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=student2-vuln-demo \
                        -Dsonar.projectName=student2-vuln-demo \
                        -Dsonar.projectVersion=1.0 \
                        -Dsonar.sources=. \
                        -Dsonar.inclusions=app.js \
                        -Dsonar.sourceEncoding=UTF-8 \
                        -Dsonar.host.url=http://192.168.119.129:9000 \
                        -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t student2-vuln-demo:latest .'
            }
        }

        stage('Run App') {
            steps {
                sh 'docker rm -f student2-vuln-app || true'
                sh 'docker run -d --name student2-vuln-app -p 3003:3000 student2-vuln-demo:latest'
            }
        }

        stage('ZAP Scan') {
            steps {
                echo 'ZAP scan stage'
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                echo 'Kubernetes deploy stage'
            }
        }
    }
}
