
pipeline {
    agent any

    environment {
        IMAGE_NAME = '24mis0129/college-events'
        GIT_REPO = 'https://github.com/Deeksha-03120/CollegeEventPortal.git'
    }

    stages {
        stage('Clone Code') {
            steps {
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        stage('Test Application') {
            steps {
                bat 'python -m unittest discover -s tests -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'Dockerhub-credentials',
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_TOKEN'
                    )
                ]) {
                    bat '''
                        @echo off
                        echo %DH_TOKEN%| docker login -u %DH_USER% --password-stdin
                        if errorlevel 1 exit /b 1
                        docker push %IMAGE_NAME%:%BUILD_NUMBER%
                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'kubeconfig',
                        variable: 'KUBECONFIG_FILE'
                    )
                ]) {
                    bat '''
                        @echo off
                        set "KUBECONFIG=%KUBECONFIG_FILE%"
                        kubectl set image deployment/college-events college-events=%IMAGE_NAME%:%BUILD_NUMBER%
                        if errorlevel 1 exit /b 1
                        kubectl rollout status deployment/college-events --timeout=180s
                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'kubeconfig',
                        variable: 'KUBECONFIG_FILE'
                    )
                ]) {
                    bat '''
                        @echo off
                        set "KUBECONFIG=%KUBECONFIG_FILE%"
                        kubectl get deployment college-events
                        kubectl get pods -l app=college-events
                        kubectl get service college-events-service
                    '''
                }
            }
        }
    }
}
