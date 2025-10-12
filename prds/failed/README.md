# Failed PRDs

PRDs in this folder failed during the agent creation process.

## Status: `failed`

These PRDs are:
- ❌ **Failed**: Processing encountered errors
- 🔍 **Needs Review**: Requires investigation and fixes
- 🔄 **Retryable**: Can be reprocessed after fixes

## Common Failure Reasons

- **Validation Errors**: PRD structure or content issues
- **Resource Limits**: Insufficient compute or storage
- **Network Issues**: Connectivity problems during deployment
- **Configuration Errors**: Invalid settings or parameters
- **Timeout**: Processing took too long

## Investigation Steps

1. **Check Logs**: Review detailed error logs
2. **Validate PRD**: Ensure PRD structure is correct
3. **Check Resources**: Verify system resources available
4. **Test Connectivity**: Ensure network access is working
5. **Review Configuration**: Check all settings and parameters

## Retry Process

To retry a failed PRD:
1. **Fix Issues**: Address the root cause of failure
2. **Update PRD**: Make necessary corrections
3. **Move to Queue**: Place back in `queue/` folder
4. **Monitor**: Watch processing in dashboard

## Error Types

- **Validation Errors**: Fix PRD structure and content
- **Resource Errors**: Increase system resources
- **Network Errors**: Check connectivity and firewall
- **Configuration Errors**: Update settings and parameters
- **Timeout Errors**: Optimize PRD complexity or increase timeout

## Prevention

To avoid failures:
- **Validate PRDs**: Use templates and validation tools
- **Monitor Resources**: Keep system resources adequate
- **Test Connectivity**: Ensure network access is stable
- **Review Config**: Double-check all settings
- **Optimize Complexity**: Keep PRDs focused and clear
