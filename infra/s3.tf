resource "aws_s3_bucket" "clinexa" {
  bucket = "clinexa-ctgov-bkt-test-run"

  tags = {
    Name        = "CT gov bucket"
    Environment = "Test"
  }
}