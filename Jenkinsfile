pipeline {
    agent any    
    environment {
        VENV_DIR = '/var/jenkins_home/workspace/Publicacion_POM/venv'
        // Establece la política CSP vacía para permitir que Jenkins muestre correctamente el HTML incrustado 
        JAVA_OPTS = "-Dhudson.model.DirectoryBrowserSupport.CSP=\"sandbox allow-scripts allow-same-origin; default-src 'none'; img-src 'self' data:; style-src 'self' 'unsafe-inline' data:; script-src 'self' 'unsafe-inline' 'unsafe-eval';\""
        // Establece las variables de allure
        APP_VERSION = '1.0.0'
        PLATFORM = 'Ubuntu-Windows 2404.1.66.0'
        BROWSER = 'Chromedriver: 130.0.6723.69'
        BUILD_RESULT = "currentBuild.currentResult"
        BUILD_DURATION = "currentBuild.durationString.replace('and counting', '').trim()"
    }
    stages {
        stage('Clean Up and Checkout ') {
            steps {
                deleteDir()
                //Clonar el repositorio Git
                git url: 'https://github.com/SAEST/Publicacion_POM.git', branch: 'main'
            }
        }
        stage('Install & Setup venv') {
            steps {
                sh "python3 -m venv ${VENV_DIR}"
            }
        }
        stage('Install Dependencies') {
            steps {
                // Activar el entorno virtual e instalar las dependencias
                sh """
                    . ${VENV_DIR}/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                """
            }
        }
        stage('Preparar ambiente') {
            steps {
                script {
                    // Generar archivo environment.properties con variables de entorno
                    def alluredir = "tests/report"
                    sh "mkdir -p ${alluredir}"
                    def pytestdir = "tests/pytestreport"
                    sh "mkdir -p ${pytestdir}"
                    sh """
                        echo 'APP_VERSION=${env.APP_VERSION}' >> ${alluredir}/environment.properties
                        echo 'PLATFORM=${env.PLATFORM}' >> ${alluredir}/environment.properties
                        echo 'BROWSER=${env.BROWSER}' >> ${alluredir}/environment.properties
                    """
                }
            }
        }
        stage('Ejecutar Pytest Selenium POM') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                sh """
                    . ${VENV_DIR}/bin/activate > /dev/null 2>&1
                    cd tests
                    pytest test_descarga_csv.py --html=pytestreport/report1.html --self-contained-html --alluredir=report
                    pytest test_public_page.py --html=pytestreport/report2.html --self-contained-html --alluredir=report
                    pytest test_public_tcsv.py --html=pytestreport/report3.html --self-contained-html --alluredir=report
                    pytest_html_merger -i /var/jenkins_home/workspace/Publicacion_POM/tests/pytestreport -o /var/jenkins_home/workspace/Publicacion_POM/tests/pytestreport/report.html
               """
                }
            }
        }
        stage('Enviar correo') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                sh """
                    . ${VENV_DIR}/bin/activate > /dev/null 2>&1
                    cd utils
                    python3 send_email.py
                """
                }
            }
        }
    }
    post {
        always {
            script {
                // Ejecuta Allure
                allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: 'tests/report']]
                
                // Define las URLs de los reportes
                def allureReportUrl = "${env.BUILD_URL}allure"
                def reportpy = "${env.BUILD_URL}execution/node/3/ws/tests/pytestreport/report.html"
                
                // Imprime las URLs en consola
                echo "El reporte de Allure está disponible en: ${allureReportUrl}"
                echo "El reporte de Pytest está disponible en: ${reportpy}"
                
                // Archiva los reportes de Pytest y datos adicionales
                archiveArtifacts artifacts: 'tests/pytestreport/report.html', allowEmptyArchive: true
                archiveArtifacts artifacts: 'tests/data/PRES_2024.csv', allowEmptyArchive: true
            }
        }
    }
}
