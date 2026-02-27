# Changelog

## [3.0.0](https://github.com/descope/django-descope/compare/django-descope-v2.1.0...django-descope-v3.0.0) (2026-02-27)


### ⚠ BREAKING CHANGES

* drop support for py3.8 ([#216](https://github.com/descope/django-descope/issues/216))

### Features

* expose descope sdk ([#153](https://github.com/descope/django-descope/issues/153)) ([81b6794](https://github.com/descope/django-descope/commit/81b6794e8b1692f7069f14e4275f63bbbe88ffae))
* pin descope/web-component ([#199](https://github.com/descope/django-descope/issues/199)) ([8af85a2](https://github.com/descope/django-descope/commit/8af85a2e1f4294cbe94080a0f1b4784d3c72e0cc))
* refactor file structure ([#39](https://github.com/descope/django-descope/issues/39)) ([c1519c5](https://github.com/descope/django-descope/commit/c1519c524073039b40d637879c07dd92fb7d5467))
* set staff and superuser from roles ([#18](https://github.com/descope/django-descope/issues/18)) ([da4dfca](https://github.com/descope/django-descope/commit/da4dfca985b3fed3047cc908a21ec251a537c9cd))
* switch to flows support ([#118](https://github.com/descope/django-descope/issues/118)) ([349a556](https://github.com/descope/django-descope/commit/349a55639a6d17968e8c6d127235e3d7fbb41572))
* **testing:** add test example with test user ([#181](https://github.com/descope/django-descope/issues/181)) ([2f9e32e](https://github.com/descope/django-descope/commit/2f9e32ef709d284ca36711810425105bc6778361))


### Bug Fixes

* add support for DESCOPE_BASE_URI ([442ecde](https://github.com/descope/django-descope/commit/442ecdef540a1cb4898cc8a275a07919eb991aa2))
* correct user information on request ([#149](https://github.com/descope/django-descope/issues/149)) ([94c29f7](https://github.com/descope/django-descope/commit/94c29f7ebe8880eebb31c33db1100ee4d54d78db))
* **deps:** pin dependency django to ==4.1.4 ([#27](https://github.com/descope/django-descope/issues/27)) ([dd3aaa1](https://github.com/descope/django-descope/commit/dd3aaa1ad83c9a0eb4297387ac1ee725661c1475))
* **deps:** pin dependency django to ==4.1.7 ([#108](https://github.com/descope/django-descope/issues/108)) ([d50a93d](https://github.com/descope/django-descope/commit/d50a93d3c85abad3ca4bd353c743df9766596e9f))
* **deps:** pin dependency django to ==4.2 ([#124](https://github.com/descope/django-descope/issues/124)) ([a926164](https://github.com/descope/django-descope/commit/a92616474cdf3df56d126bccbfd7ff5be4074ddb))
* **deps:** pin dependency django to v4.1.4 ([#56](https://github.com/descope/django-descope/issues/56)) ([6db74a3](https://github.com/descope/django-descope/commit/6db74a30e2a8c2bb58523a79197d8d4980e694f2))
* **deps:** update dependency descope to v0.3.0 ([#32](https://github.com/descope/django-descope/issues/32)) ([d397687](https://github.com/descope/django-descope/commit/d397687e95e2f249e6a1918a0313b8131f665993))
* **deps:** update dependency descope to v0.9.0 ([#78](https://github.com/descope/django-descope/issues/78)) ([e51980c](https://github.com/descope/django-descope/commit/e51980c0c580c23278d99f67014da84d8ba9b9b4))
* **deps:** update dependency descope to v0.9.1 ([#96](https://github.com/descope/django-descope/issues/96)) ([504776b](https://github.com/descope/django-descope/commit/504776b5e480e9d3bacc1da15c527f07b22b072d))
* **deps:** update dependency descope to v1 ([#109](https://github.com/descope/django-descope/issues/109)) ([de3a8e8](https://github.com/descope/django-descope/commit/de3a8e81945c976f8498e9d172f7efd42c618e63))
* **deps:** update dependency descope to v1.1.0 ([#125](https://github.com/descope/django-descope/issues/125)) ([8fbe8a0](https://github.com/descope/django-descope/commit/8fbe8a057da40c5e212168e3c3c44e91a93b6568))
* **deps:** update dependency descope to v1.1.1 ([#129](https://github.com/descope/django-descope/issues/129)) ([2e326c6](https://github.com/descope/django-descope/commit/2e326c64067cd7ef3d80560348e22d71e3df20f6))
* **deps:** update dependency descope to v1.5.0 ([#131](https://github.com/descope/django-descope/issues/131)) ([0884fe2](https://github.com/descope/django-descope/commit/0884fe2eb74bbd561ea3a8d44e24270f78c7c2c8))
* **deps:** update dependency django to v3.2.16 ([#8](https://github.com/descope/django-descope/issues/8)) ([b639a27](https://github.com/descope/django-descope/commit/b639a274872a57837a95a1f458083756b45a4571))
* **deps:** update dependency django to v4.1.7 [security] ([#104](https://github.com/descope/django-descope/issues/104)) ([ebb2264](https://github.com/descope/django-descope/commit/ebb226496cc82388cfa65f667475be962664ce34))
* **deps:** update dependency django to v4.2.1 [security] ([#133](https://github.com/descope/django-descope/issues/133)) ([691d81c](https://github.com/descope/django-descope/commit/691d81ca7fe317a8c4f87ca6a622f6b682008eaa))
* **deps:** update dependency django to v4.2.16 [security] ([#205](https://github.com/descope/django-descope/issues/205)) ([d997e4a](https://github.com/descope/django-descope/commit/d997e4a439461b826a82e729f1d2316c36aae346))
* **deps:** update dependency django to v4.2.18 [security] ([#217](https://github.com/descope/django-descope/issues/217)) ([cc39ee8](https://github.com/descope/django-descope/commit/cc39ee86a5ad2bd24572a11f73745d9f4d25052d))
* **deps:** update dependency django to v4.2.20 [security] ([#242](https://github.com/descope/django-descope/issues/242)) ([19e189c](https://github.com/descope/django-descope/commit/19e189c827b4ad40ced4288d18209728e993154a))
* **deps:** update dependency django to v4.2.21 [security] ([#289](https://github.com/descope/django-descope/issues/289)) ([37e4462](https://github.com/descope/django-descope/commit/37e4462adbddff659e6ee6e03b6de7b9da0bb0f8))
* **deps:** update dependency django to v4.2.22 [security] ([#321](https://github.com/descope/django-descope/issues/321)) ([23ff2e6](https://github.com/descope/django-descope/commit/23ff2e6929d3db151f57c4329a72de434de62dd3))
* **deps:** update dependency django to v4.2.3 [security] ([#161](https://github.com/descope/django-descope/issues/161)) ([c535df7](https://github.com/descope/django-descope/commit/c535df73e8830993e39058f8105dce943618c707))
* **deps:** update dependency django to v4.2.7 [security] ([#178](https://github.com/descope/django-descope/issues/178)) ([a2aea1f](https://github.com/descope/django-descope/commit/a2aea1fea51da6ad2559121c1ff129827e8e8450))
* **deps:** update dependency django to v5.2.7 [security] ([#363](https://github.com/descope/django-descope/issues/363)) ([0e50482](https://github.com/descope/django-descope/commit/0e50482956acd56fd566d4e6f4dbac5bc54a7beb))
* ensure Descope middleware order ([#150](https://github.com/descope/django-descope/issues/150)) ([e64d67a](https://github.com/descope/django-descope/commit/e64d67a095286a7cf39e6ded73748213b3b49343))
* fixing store_jwt view ([#185](https://github.com/descope/django-descope/issues/185)) ([ed49892](https://github.com/descope/django-descope/commit/ed49892ad9d60a8a4a6f16599893661266f2f89a))
* make renovate pickup web-component version ([#222](https://github.com/descope/django-descope/issues/222)) ([d50645c](https://github.com/descope/django-descope/commit/d50645c6ca5b5ff6e8071101e7e67667a8541f44))
* **middleware:** remove redundant call for response ([#136](https://github.com/descope/django-descope/issues/136)) ([b3e2bc7](https://github.com/descope/django-descope/commit/b3e2bc7af99a3dad7fbaa17849f3c1a09af99f1a))
* update descope api ([#111](https://github.com/descope/django-descope/issues/111)) ([505c6ce](https://github.com/descope/django-descope/commit/505c6ce59cecaab94afa5eb0ec49c72a0a5d41fa))
* uri bug and add custom username claim option ([#220](https://github.com/descope/django-descope/issues/220)) ([e83b9c6](https://github.com/descope/django-descope/commit/e83b9c6cfb7a2a6f9414cf07219dd0067247f830))


### Miscellaneous Chores

* drop support for py3.8 ([#216](https://github.com/descope/django-descope/issues/216)) ([e3a5556](https://github.com/descope/django-descope/commit/e3a5556a172de8baa8a197da26a533ed6020c92f))
