package com.optimized.paiementmanagement.repository;

import com.optimized.paiementmanagement.model.CompteBancaire;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Bank Account Repository
 */
@Repository
public interface CompteBancaireRepository extends JpaRepository<CompteBancaire, Long> {
    
    Optional<CompteBancaire> findByNumeroCompte(String numeroCompte);
    
    boolean existsByNumeroCompte(String numeroCompte);
}
