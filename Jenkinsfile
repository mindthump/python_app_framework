pipeline {
  agent {
    kubernetes {
      cloud 'kubernetes'
      nodeSelector 'kubernetes.io/hostname=lima-rancher-desktop'
      yaml '''
kind: Pod
spec:
  volumes:
    - name: appdata
      emptyDir: {}
  containers:
    - name: toolkit
      image: toolkit:tini
      imagePullPolicy: Never
      command:
        - sleep
      args:
        - 1d
      volumeMounts:
        - name: appdata
          mountPath: /data
'''
    }
  }


  stages {
    stage('Main') {
      steps {
        container ('toolkit') {
          sh 'uname -a; env; pwd; ls -al'
        }
        container ('jnlp') {
          sh 'uname -a; env; pwd; ls -al'
        }
      }
    }
  }
}
