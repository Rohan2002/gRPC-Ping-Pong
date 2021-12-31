check-grpc:
	python3 -c "import grpc; print(grpc.__version__)"
proto-compile:
	 python -m grpc_tools.protoc -I ./protos --python_out=. --grpc_python_out=. ./protos/ping-pong.proto