pipeline {
  agent {
    kubernetes {
      cloud 'kubernetes-rancher-desktop'
      nodeSelector 'kubernetes.io/hostname=lima-rancher-desktop'
      yaml '''
kind: Pod
spec:
  volumes:
    - name: appdata
      emptyDir: {}
  containers:
    - name: toolkit
      image: mindthump/toolkit
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
          sh 'uname -a'
        }
        container ('jnlp') {
          sh 'uname -a'
          sh 'ls -lR /opt'
        }
      }
    }
  }
}
