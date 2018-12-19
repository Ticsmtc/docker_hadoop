#!/usr/bin/env bash

touch /etc/profile.d/jdk_config.sh

JDK_PROFILE=/etc/profile.d/jdk_config.sh
JAVA_HOME=/root/amber/jdk1.8


echo "#!/usr/bin/env bash" >> $JDK_PROFILE
echo "export JAVA_HOME=/root/amber/jdk1.8" >> $JDK_PROFILE
echo "export PATH=$PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/bin" >> $JDK_PROFILE
echo "export CLASSPATH=$CLASSPATH:.:$JAVA_HOME/lib:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar" >> $JDK_PROFILE


exit 0
