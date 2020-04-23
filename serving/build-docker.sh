echo Builds an image using Tensorflow 2.0 and the models at models/eng-cat/
if [ "$1" = "prod" ];
    then
        buildType="prod"
        cp Dockerfile DockerfileBuild
    else
        buildType='dev'
        grep -v tensorflow-2.1.0 Dockerfile > DockerfileBuild
fi
echo "Build type: $buildType"
pushd ..
docker build -t traductor-eng-cat . -f serving/DockerfileBuild
popd
docker image ls | grep traductor-eng-cat
