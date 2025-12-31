
### Infrastructure (Terraform)
- **S3 Bucket**: Raw data storage
  - `/staging/YYYY-MM-DD/`: Individual Parquet files from API calls
  - `/compacted/YYYY-MM-DD/`: Compacted daily files (archival)
- **EC2/ECS**: Run your existing Python code
- **RDS Postgres**: Target database
- **IAM Roles**: Permissions for S3 access

### Application Components
- **Data Loader**: Reads from S3, loads to Postgres
- **Compaction Service**: Async cleanup process (separate from critical path)

---

## Phase 1: Infrastructure Setup (Terraform)

### Tasks
3. Configure RDS Postgres instance (or use existing)
4. Create EC2 instance or ECS task definition
5. Set up VPC, security groups, networking

### Deliverables
- `main.tf`: Core infrastructure
- `variables.tf`: Configurable parameters
- `outputs.tf`: Important values (bucket name, DB endpoint, etc.)

---

## Phase 2: Modify Existing Code for S3

### Critical Path Pipeline
```
API → JSON → Parquet → S3 staging → Read from S3 → DataFrame → Postgres
```

### Tasks
1. **Update API fetcher**
   - Replace local file writes with S3 writes (boto3)
   - Keep same Parquet conversion logic
   - Write to `s3://bucket/staging/YYYY-MM-DD/batch_HHMMSS.parquet`

2. **Update data loader**
   - Read Parquet files from S3 instead of local disk
   - Convert to DataFrame
   - Load to Postgres (keep existing logic)

3. **Add error handling**
   - Retry logic for S3 operations
   - Logging for debugging
   - Handle network failures gracefully

### Deliverables
- Modified Python scripts
- Configuration file for S3 bucket names, paths
- Requirements.txt with boto3, s3fs

---

## Phase 3: Deploy & Test Critical Path

### Tasks
1. Deploy code to EC2/ECS
2. Test end-to-end: API → S3 → Postgres
3. Verify data availability and correctness
4. Monitor costs (S3 requests, data transfer)
5. Set up basic monitoring/alerting

### Success Criteria
- Data flows from API to Postgres successfully
- Latency acceptable
- No data loss
- Costs within budget

---

## Phase 4: Async Compaction Service (Optional/Later)

### Non-Critical Path
```
Separate process: Read staging files → Compact → Write to /compacted/ → Delete staging
```

### Tasks
1. **Create compaction script**
   - List files in staging for target date
   - Download/stream and concatenate Parquet files
   - Write compacted file to `s3://bucket/compacted/YYYY-MM-DD.parquet`
   - Delete original staging files after verification

2. **Schedule compaction**
   - Cron job on EC2, or
   - Scheduled ECS task, or
   - EventBridge + Lambda (if you want to learn it)

3. **Add safeguards**
   - Don't compact today's data (work on yesterday's)
   - Verify compacted file before deleting staging files
   - Handle partial failures

### Deliverables
- Compaction script
- Scheduling configuration
- Monitoring for compaction job health

---

## Cost Considerations

### S3 Costs
- **Storage**: ~$0.023/GB/month (very cheap)
- **PUT requests**: $0.005 per 1,000 requests
- **GET requests**: $0.0004 per 1,000 requests
- **Data transfer**: Out to internet costs money, within AWS region is cheap/free

### Optimization Tips
- Batch smaller API responses before writing to S3
- Use S3 lifecycle policies to move old data to cheaper storage (Glacier)
- Monitor request counts - they add up faster than storage
- Consider using S3 Express One Zone for hot data (faster, more expensive)

---
The Pandas → PyArrow Thing I Mentioned Earlier
Looking at your extractor:
pythondf = pd.DataFrame(data)
table = pa.Table.from_pandas(df)
And then your transformer:
pythonprotocols = df['protocolSection'].tolist()
for protocol in protocols:
    if isinstance(protocol, str):
        protocol = json.loads(protocol)
So the nested JSON is getting stringified by pandas when you save it as parquet, and then you're parsing it back in the transformer. This works, but it's inefficient:

Larger parquet files (JSON strings don't compress as well)
Extra serialization/deserialization overhead
Loses parquet's native nested type support

Not a blocker at your scale, but worth noting. If you wanted to optimize later, you'd use PyArrow's native struct types to preserve the nesting in parquet.
Potential Issues I'd Watch For
1. Memory in Transformer
You're accumulating everything in memory:
pythonself.studies_data.append(study_data)
self.sponsors_data.append(...)
With 1,000 studies per file × ~7 KB each = manageable. But if you ever process multiple files at once or scale up, this could blow up. Consider yielding batches or writing incrementally.
2. The Deduplication Check
pythonif not any(s['sponsor_key'] == sponsor_key for s in self.sponsors_data):
This is O(n²) - for every sponsor, you're scanning the entire list. With thousands of sponsors across 557k studies, this could get slow. Consider using a set:
pythonseen_sponsor_keys = set()

if sponsor_key not in seen_sponsor_keys:
    seen_sponsor_keys.add(sponsor_key)
    self.sponsors_data.append(...)
Same for conditions, interventions, sites.
3. Incremental Loading Strategy
How are you handling daily incremental loads to Postgres? Are you:

TRUNCATE + full reload?
UPSERT on keys?
INSERT new + UPDATE changed?

Your keys are deterministic, so UPSERT should work cleanly. Just make sure your Postgres load handles it.
4. The tolist() Calls
pythonif hasattr(collaborators, 'tolist'):
    collaborators = collaborators.tolist()
This suggests pandas is sometimes returning numpy arrays or Series instead of lists. That's a side effect of how pandas handles nested data. If you used PyArrow for extraction, this wouldn't be an issue.
Overall Take
This is well-architected! The separation of concerns is clean:

Extractor = resilient data acquisition
Transformer = business logic + normalization
Loading (presumably separate) = database interaction

The complexity is where it should be - in the transformer handling gnarly nested JSON. The storage optimization question you started with is genuinely not your bottleneck here.
How are you planning to handle the Postgres loading part? That's where things can get interesting with 557k studies.RetryClaude can make mistakes. Please double-check responses. Sonnet 4.5

## Open Questions / Decisions Needed

- [ ] EC2 vs ECS vs Lambda? (EC2 simplest for your use case)
- [ ] How often do you hit the API? (determines # of files)
- [ ] Postgres on RDS or self-hosted?
- [ ] What's your budget for AWS costs?
- [ ] Monitoring: CloudWatch, Datadog, or something else?
- [ ] Do you need the compacted files, or just for cost savings?


