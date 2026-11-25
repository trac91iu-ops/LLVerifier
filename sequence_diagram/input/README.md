# Protocol sequence diagrams

Each diagram describes protocol actions, enabling conditions, and state changes. Action blocks are not a mandatory global execution order. No checker properties or fairness constraints are included.

New diagrams are derived from the golden `rules.maude` files, including transition guards and imported event-processing semantics. They are model-derived inputs, not independently authored protocol descriptions.paper

The existing handwritten Philips input and its annotation are preserved. It is a format reference rather than a complete transcription: its diagram omits some golden-model guards and timing behavior, and its join branch requires a nonempty owner whereas the golden join rule does not.

| Golden protocol | Input | Source |
|---|---|---|
| A2A | [A2A/diagram.md](A2A/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/A2A/rules.maude) |
| Aqara | [Aqara/diagram.md](Aqara/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Aqara/rules.maude) |
| August | [August/diagram.md](August/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/August/rules.maude) |
| Beurer | [Beurer/diagram.md](Beurer/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Beurer/rules.maude) |
| Broadlink | [Broadlink/diagram.md](Broadlink/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Broadlink/rules.maude) |
| CloudEdgeCAC | [CloudEdgeCAC/diagram.md](CloudEdgeCAC/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/CloudEdgeCAC/rules.maude) |
| CloudEdgeRTE | [CloudEdgeRTE/diagram.md](CloudEdgeRTE/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/CloudEdgeRTE/rules.maude) |
| Dyson | [Dyson/diagram.md](Dyson/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Dyson/rules.maude) |
| Ezviz | [Ezviz/diagram.md](Ezviz/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Ezviz/rules.maude) |
| Govee | [Govee/diagram.md](Govee/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Govee/rules.maude) |
| Huawei | [Huawei/diagram.md](Huawei/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Huawei/rules.maude) |
| Imou | [Imou/diagram.md](Imou/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Imou/rules.maude) |
| Kevo | [Kevo/diagram.md](Kevo/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Kevo/rules.maude) |
| MQTTFlaw1 | [MQTTFlaw1/diagram.md](MQTTFlaw1/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/MQTTFlaw1/rules.maude) |
| MaagKwikset | [MaagKwikset/diagram.md](MaagKwikset/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/MaagKwikset/rules.maude) |
| MaagLevel | [MaagLevel/diagram.md](MaagLevel/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/MaagLevel/rules.maude) |
| Meross | [Meross/diagram.md](Meross/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Meross/rules.maude) |
| Midea | [Midea/diagram.md](Midea/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Midea/rules.maude) |
| Netvue | [Netvue/diagram.md](Netvue/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Netvue/rules.maude) |
| Philips | [philips/diagram.md](philips/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Philips/rules.maude) |
| Sunlogin | [Sunlogin/diagram.md](Sunlogin/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Sunlogin/rules.maude) |
| Switchbot | [Switchbot/diagram.md](Switchbot/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Switchbot/rules.maude) |
| TPLink | [TPLink/diagram.md](TPLink/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/TPLink/rules.maude) |
| TuyaCAC | [TuyaCAC/diagram.md](TuyaCAC/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/TuyaCAC/rules.maude) |
| TuyaMatter | [TuyaMatter/diagram.md](TuyaMatter/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/TuyaMatter/rules.maude) |
| Wemo | [Wemo/diagram.md](Wemo/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Wemo/rules.maude) |
| Xiaomi | [Xiaomi/diagram.md](Xiaomi/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/Xiaomi/rules.maude) |
| delegationFlaw1 | [delegationFlaw1/diagram.md](delegationFlaw1/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/delegationFlaw1/rules.maude) |
| delegationFlaw2 | [delegationFlaw2/diagram.md](delegationFlaw2/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/delegationFlaw2/rules.maude) |
| iRobot | [iRobot/diagram.md](iRobot/diagram.md) | [rules.maude](../../benchmark/golden_data/formalModels/iRobot/rules.maude) |

## Checks

All 30 protocols have a diagram: 29 newly generated files plus the unchanged Philips reference. For the 29 new files, all distinct action names in the source models are accounted for, including explicit notes for unreachable handlers. Mermaid block balance and participant references were checked. These checks do not establish semantic equivalence; diagrams have not been rendered or passed through the model-generation pipeline.
