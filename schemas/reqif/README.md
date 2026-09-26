# Vendored ReqIF 1.2 schema

The OMG ReqIF 1.2 schema (`reqif.xsd`, namespace 20110401) and every schema it imports: the OMG XHTML driver and the
W3C XHTML Modularization and `xml.xsd` modules. Files are unmodified copies. `sources.json` records each file's origin
URL, and `catalog.xml` maps those URLs to the local copies so validation needs no network:

```sh
XML_CATALOG_FILES=schemas/reqif/catalog.xml xmllint --nonet --noout --schema schemas/reqif/reqif.xsd docs/requirements.reqif
```

Why vendor: CI once failed because omg.org didn't serve `driver.xsd` at that moment, so the schema couldn't compile.
The schemas are published by the OMG and W3C for use in validation; see each file's header for its terms.
