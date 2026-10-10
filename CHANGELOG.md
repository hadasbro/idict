# Change log

### v1.0.0 - current
* Stabilized schema enforcement for `THROW` mode across `update`, `setdefault`, `|`, and `|=`
* Fixed validation of mandatory (`...`) keys against the declared schema
* Isolated internal state per `Idict` instance
* Removed shared mutable defaults between instances
* Added regression tests for release-critical API guarantees
* Distribution package name is now `idict-schema` (import path remains `idict`)
* `pickle` serialization is intentionally unsupported with a clear error message

### v1.0.1-SNAPSHOT
* First, non tested snapshot version
