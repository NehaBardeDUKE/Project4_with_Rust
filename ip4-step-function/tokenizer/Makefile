format:
	cargo fmt --quiet

lint:
	cargo clippy --quiet

test:
	cargo test --quiet

run:
	cargo run 

release:
	cargo lambda build --release --target x86_64-unknown-linux-musl

deploy:
	cargo lambda deploy --iam-role arn:aws:iam::599412038047:role/lambdaefs --region us-east-1 --verbose

invoke:
	cargo lambda invoke --remote \
  		--data-ascii '{"stmt": "start"}' \
  		--output-format json \
  		tokenizer
			
all: format lint test run