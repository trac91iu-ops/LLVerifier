# LL-Verifier

## Roadmap
- Source code: `src/`
- Benchmark: `benchmark/`
- Prompt for generating Maude directly in ablation evaluation: in `src/prompts_text.py`
- Attack traces in Section 5: `output/trace`
- Vendor response: `Vendor-Response/`
- PoC videos: `PoC-Videos/`

## Source Code

### Prerequisites
+ Python3.8+
+ maude v3.2.2+
+ set environment variable $EDITOR
+ `cp lib/preludePatched.maude /usr/share/maude/prelude.maude`
+ `cp configs/config.yaml.sample configs/config.yaml` , then edit configs/config.yaml
+ `bash scripts/bootstrap.sh`
+ `source venv/bin/activate`

### Usage

#### Generation
`python src/main.py <path_to_protocol_text>`

#### Checking:
`maude output/XXX/checker.maude`

## Vendor Response
- Philips Hue RTE
![](./Vendor-Response/hue_reply1.png)
![](./Vendor-Response/hue_reply2.png)
- Broadlink RTE
![Broadlink RTE](./Vendor-Response/Broadlink_reply.png)
- Imou RTE
![Imou RTE](./Vendor-Response/Imou_reply.png)
- Aqara (Flaw 8)
![Aqara RTE](./Vendor-Response/aqara_reply.png)
- Tuya (Flaw 9)
![](./Vendor-Response/tuya_reply1.png)
- Beurer RTE
![Beurer RTE](./Vendor-Response/beurer_reply.png)
- Govee RTE
![Govee RTE](./Vendor-Response/govee_reply.png)
- Meross RTE
![](./Vendor-Response/meross_reply.png)
- Oray RTE
![](./Vendor-Response/oray_reply.png)
- Switchbot RTE
![](./Vendor-Response/switchbot_reply.png)
- Wiz RTE
![](./Vendor-Response/wiz_reply.png)
- Xiaomi CAC
![](./Vendor-Response/xiaomi_reply.png)
