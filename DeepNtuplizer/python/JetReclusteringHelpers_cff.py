import FWCore.ParameterSet.Config as cms

def SetupClusteringPFChargedJets(process,pfChgJetPtMin=5,genJetCollection="slimmedGenJets",
  addPFChgJets=True,addPFChgJetsCHS=False,addPFChgJetsPuppi=False):

  ###########################################################################
  #
  # Make function wrapper around PatAlgos helper functions
  #
  ###########################################################################
  from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask, addToProcessAndTask
  def addProcessAndTask(process, label, module):
    task = getPatAlgosToolsTask(process)
    addToProcessAndTask(label, module, process, task)

  ###########################################################################
  #
  # Prepare jet clustering inputs
  #
  ###########################################################################
  addProcessAndTask(process, "packedPFCandidatesChg",cms.EDFilter("CandPtrSelector",
      src = cms.InputTag("packedPFCandidates"),
      cut = cms.string("charge != 0")
    )
  )

  if addPFChgJetsCHS:
    from CommonTools.ParticleFlow.pfCHS_cff import pfCHS
    addProcessAndTask(process, "pfChgCHS", pfCHS.clone(
        src = "packedPFCandidatesChg",
      )
    )

  if addPFChgJetsPuppi:
    from CommonTools.PileupAlgos.Puppi_cff import puppi
    addProcessAndTask(process, "packedpuppi", puppi.clone(
        useExistingWeights = True,
        candName = 'packedPFCandidates',
        vertexName = 'offlineSlimmedPrimaryVertices'
      )
    )

  ###########################################################################
  #
  # Jet clustering
  #
  ###########################################################################
  if addPFChgJets:
    from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
    addProcessAndTask(process, "ak4PFChgJets", ak4PFJets.clone(
        src = "packedPFCandidatesChg",
        jetPtMin=pfChgJetPtMin,
        doAreaFastjet = True
      )
    )

  if addPFChgJetsCHS:
    from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsCHS
    addProcessAndTask(process, "ak4PFChgJetsCHS", ak4PFJetsCHS.clone(
        src = "pfChgCHS",
        jetPtMin=pfChgJetPtMin,
        doAreaFastjet = True
      )
    )

  if addPFChgJetsPuppi:
    from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi
    addProcessAndTask(process, "ak4PFChgJetsPuppi", ak4PFJetsPuppi.clone(
        src = "packedPFCandidatesChg",
        srcWeights = "packedpuppi",
        jetPtMin=pfChgJetPtMin,
        doAreaFastjet = True
      )
    )

  ###########################################################################
  #
  # PAT-ify the jet collections
  #
  ###########################################################################
  jetCorrectionsAK4 = None
  btagDiscriminators = None
  btagInfos = None

  from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection, updateJetCollection

  if addPFChgJets:
    #
    # AK4 PF Chg jets
    # Collection name: selectedUpdatedPatJetsAK4PFChg
    #
    addJetCollection(
      process,
      labelName          = "AK4PFChg",
      jetSource          = cms.InputTag("ak4PFChgJets"),
      algo               = "ak", #name of algo must be in this format
      rParam             = 0.4,
      pvSource           = cms.InputTag("offlineSlimmedPrimaryVertices"),
      pfCandidates       = cms.InputTag("packedPFCandidates"),
      svSource           = cms.InputTag("slimmedSecondaryVertices"),
      muSource           = cms.InputTag("slimmedMuons"),
      elSource           = cms.InputTag("slimmedElectrons"),
      genJetCollection   = cms.InputTag(genJetCollection),
      genParticles       = cms.InputTag("prunedGenParticles"),
      jetCorrections     = jetCorrectionsAK4,
    )
    updateJetCollection(
      process,
      labelName = "AK4PFChg",
      jetSource = cms.InputTag("selectedPatJetsAK4PFChg"),
      pfCandidates = cms.InputTag('packedPFCandidates'),
      pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
      svSource = cms.InputTag('slimmedSecondaryVertices'),
      muSource = cms.InputTag('slimmedMuons'),
      elSource = cms.InputTag('slimmedElectrons'),
      jetCorrections = jetCorrectionsAK4,
      btagDiscriminators = btagDiscriminators,
      btagInfos = btagInfos,
      explicitJTA = False
    )

  #
  # AK4 PF Chg CHS jets
  # Collection name: selectedUpdatedPatJetsAK4PFChgCHS
  #
  if addPFChgJetsCHS:
    addJetCollection(
      process,
      postfix            = "",
      labelName          = "AK4PFChgCHS",
      jetSource          = cms.InputTag("ak4PFChgJetsCHS"),
      algo               = "ak", #name of algo must be in this format
      rParam             = 0.4,
      pvSource           = cms.InputTag("offlineSlimmedPrimaryVertices"),
      pfCandidates       = cms.InputTag("packedPFCandidates"),
      svSource           = cms.InputTag("slimmedSecondaryVertices"),
      muSource           = cms.InputTag("slimmedMuons"),
      elSource           = cms.InputTag("slimmedElectrons"),
      genJetCollection   = cms.InputTag(genJetCollection),
      genParticles       = cms.InputTag("prunedGenParticles"),
      jetCorrections     = jetCorrectionsAK4,
    )
    updateJetCollection(
      process,
      labelName = "AK4PFChgCHS",
      jetSource = cms.InputTag("selectedPatJetsAK4PFChgCHS"),
      pfCandidates = cms.InputTag('packedPFCandidates'),
      pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
      svSource = cms.InputTag('slimmedSecondaryVertices'),
      muSource = cms.InputTag('slimmedMuons'),
      elSource = cms.InputTag('slimmedElectrons'),
      jetCorrections = jetCorrectionsAK4,
      btagDiscriminators = btagDiscriminators,
      btagInfos = btagInfos,
      explicitJTA = False
    )

  #
  # AK4 PF Chg Puppi jets
  # Collection name: selectedUpdatedPatJetsAK4PFChgPuppi
  #
  if addPFChgJetsPuppi:
    addJetCollection(
      process,
      postfix            = "",
      labelName          = "AK4PFChgPuppi",
      jetSource          = cms.InputTag("ak4PFChgJetsPuppi"),
      algo               = "ak", #name of algo must be in this format
      rParam             = 0.4,
      pvSource           = cms.InputTag("offlineSlimmedPrimaryVertices"),
      pfCandidates       = cms.InputTag("packedPFCandidates"),
      svSource           = cms.InputTag("slimmedSecondaryVertices"),
      muSource           = cms.InputTag("slimmedMuons"),
      elSource           = cms.InputTag("slimmedElectrons"),
      genJetCollection   = cms.InputTag(genJetCollection),
      genParticles       = cms.InputTag("prunedGenParticles"),
      jetCorrections     = jetCorrectionsAK4,
    )
    process.patJetFlavourAssociationAK4PFChgPuppi.weights = cms.InputTag("packedpuppi")

    updateJetCollection(
      process,
      labelName = "AK4PFChgPuppi",
      jetSource = cms.InputTag("selectedPatJetsAK4PFChgPuppi"),
      pfCandidates = cms.InputTag('packedPFCandidates'),
      pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
      svSource = cms.InputTag('slimmedSecondaryVertices'),
      muSource = cms.InputTag('slimmedMuons'),
      elSource = cms.InputTag('slimmedElectrons'),
      jetCorrections = jetCorrectionsAK4,
      btagDiscriminators = btagDiscriminators,
      btagInfos = btagInfos,
      explicitJTA = False
    )


  return process
