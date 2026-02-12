package com.optimized.paiementmanagement.service.impl;

import com.optimized.paiementmanagement.dto.CompteBancaireRequestDTO;
import com.optimized.paiementmanagement.dto.CompteBancaireResponseDTO;
import com.optimized.paiementmanagement.exception.ResourceAlreadyExistsException;
import com.optimized.paiementmanagement.exception.ResourceNotFoundException;
import com.optimized.paiementmanagement.model.CompteBancaire;
import com.optimized.paiementmanagement.repository.CompteBancaireRepository;
import com.optimized.paiementmanagement.service.CompteBancaireService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Bank Account Service Implementation - Optimized
 */
@Service
@Transactional
@RequiredArgsConstructor
@Slf4j
public class CompteBancaireServiceImpl implements CompteBancaireService {
    
    private final CompteBancaireRepository compteBancaireRepository;
    
    @Override
    public CompteBancaireResponseDTO createCompte(CompteBancaireRequestDTO requestDTO) {
        log.info("Creating bank account: {}", requestDTO.getNumeroCompte());
        
        // Check if account already exists
        if (compteBancaireRepository.existsByNumeroCompte(requestDTO.getNumeroCompte())) {
            throw new ResourceAlreadyExistsException("CompteBancaire", "numeroCompte", requestDTO.getNumeroCompte());
        }
        
        CompteBancaire compte = CompteBancaire.builder()
                .numeroCompte(requestDTO.getNumeroCompte())
                .solde(requestDTO.getSolde())
                .titulaire(requestDTO.getTitulaire())
                .typeCompte(requestDTO.getTypeCompte())
                .status(CompteBancaire.CompteStatus.ACTIVE)
                .build();
        
        CompteBancaire savedCompte = compteBancaireRepository.save(compte);
        
        log.info("Bank account created successfully");
        
        return mapToResponseDTO(savedCompte);
    }
    
    @Override
    @Transactional(readOnly = true)
    public CompteBancaireResponseDTO getCompteById(Long id) {
        log.debug("Fetching bank account by ID: {}", id);
        
        CompteBancaire compte = compteBancaireRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("CompteBancaire", "id", id));
        
        return mapToResponseDTO(compte);
    }
    
    @Override
    @Transactional(readOnly = true)
    public CompteBancaireResponseDTO getCompteByNumero(String numeroCompte) {
        log.debug("Fetching bank account by number: {}", numeroCompte);
        
        CompteBancaire compte = compteBancaireRepository.findByNumeroCompte(numeroCompte)
                .orElseThrow(() -> new ResourceNotFoundException("CompteBancaire", "numeroCompte", numeroCompte));
        
        return mapToResponseDTO(compte);
    }
    
    @Override
    @Transactional(readOnly = true)
    public List<CompteBancaireResponseDTO> getAllComptes() {
        log.debug("Fetching all bank accounts");
        
        return compteBancaireRepository.findAll().stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }
    
    @Override
    public CompteBancaireResponseDTO updateSolde(Long id, BigDecimal nouveauSolde) {
        log.info("Updating account {} balance to {}", id, nouveauSolde);
        
        CompteBancaire compte = compteBancaireRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("CompteBancaire", "id", id));
        
        compte.setSolde(nouveauSolde);
        CompteBancaire updatedCompte = compteBancaireRepository.save(compte);
        
        log.info("Account balance updated successfully");
        
        return mapToResponseDTO(updatedCompte);
    }
    
    @Override
    public void deleteCompte(Long id) {
        log.info("Deleting bank account: {}", id);
        
        if (!compteBancaireRepository.existsById(id)) {
            throw new ResourceNotFoundException("CompteBancaire", "id", id);
        }
        
        compteBancaireRepository.deleteById(id);
        
        log.info("Bank account deleted successfully");
    }
    
    private CompteBancaireResponseDTO mapToResponseDTO(CompteBancaire compte) {
        return CompteBancaireResponseDTO.builder()
                .id(compte.getId())
                .numeroCompte(compte.getNumeroCompte())
                .solde(compte.getSolde())
                .titulaire(compte.getTitulaire())
                .typeCompte(compte.getTypeCompte())
                .status(compte.getStatus().name())
                .createdDate(compte.getCreatedDate())
                .build();
    }
}
