
pipeline {
    agent any

    environment {
        IMAGE_NAME = '24mis0129/college-events'
        GIT_REPO = 'https://github.com/Deeksha-03120/CollegeEventPortal.git'
        PYTHON_EXE = 'C:\\Users\\SENTHIL\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }

    stages {
        stage('Clone Code') {
            steps {
                echo 'Source code checked out by Jenkins from GitHub.'
                bat 'git log -1 --oneline'
            }
        }

        stage('Test Application') {
            steps {
                bat '''
                    "%PYTHON_EXE%" --version
                    "%PYTHON_EXE%" -m unittest discover -s tests -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    docker version
                    docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .
                '''
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
                        echo Logging in to Docker Hub...
                        echo %DH_TOKEN%| docker login -u %DH_USER% --password-stdin
                        if errorlevel 1 exit /b 1

                        docker push %IMAGE_NAME%:%BUILD_NUMBER%
                        if errorlevel 1 exit /b 1

                        docker logout
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

                        kubectl apply -f k8s/
                        if errorlevel 1 exit /b 1

                        kubectl rollout status deployment/college-events --timeout=120s
                        if errorlevel 1 exit /b 1

                        kubectl set image deployment/college-events college-events=%IMAGE_NAME%:%BUILD_NUMBER%
                        if errorlevel 1 exit /b 1

                        kubectl rollout status deployment/college-events --timeout=180s
                        if errorlevel 1 (
                            echo Deployment failed. Rolling back to the previous stable revision...
                            kubectl rollout undo deployment/college-events
                            kubectl rollout status deployment/college-events --timeout=180s
                            exit /b 1
                        )
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
                        kubectl get endpoints college-events-service
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed, image pushed, and Kubernetes deployment verified.'
        }
        failure {
            echo 'FAILURE: Check the failed stage in Console Output.'
        }
    }
}
