# Evidence and provenance

`evidence_preservation.py` creates an acquisition receipt containing the
requested and final URL, response status and headers, capture parameters,
package version, timestamps, optional-step results, and SHA-256 hashes for local
artefacts.

The receipt can prove that a listed local artefact still matches the bytes hashed
when the receipt was written. It can also show what the tool recorded about the
request and response.

It does not prove:

- who operated the tool or whether they were authorised;
- that the remote server’s representation was complete or authentic;
- continuous custody after acquisition;
- that a screenshot reproduces every network response;
- that an independent archive accepted a submission;
- legal admissibility or the truth of the captured claim.

Keep the receipt beside its artefacts, restrict write access, and verify hashes
before analysis, transfer, and disclosure. Record transfers, access, corrections,
and disposition in a separately designed custody-event log when that level of
assurance is required. Calling a receipt a chain does not add any links.
